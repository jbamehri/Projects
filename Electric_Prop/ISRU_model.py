
"""
/.
Authored by: Joud Bamehriz
Refernces used are in the refernces section of the report
"""
import math
from collections import OrderedDict

# -------------------------
# Physical Constants
# -------------------------
q_e = 1.602176634e-19       # elementary charge (C)
k_B = 1.380649e-23          # Boltzmann constant (J/K)
amu_kg = 1.66053906660e-27  # atomic mass unit (kg)
m_e = 9.1093837015e-31      # electron mass (kg)
pi = math.pi
g_0= 9.80665                #acceleration of gravity (m/s^2)

# -------------------------
# Thruster Inputs
# -------------------------
Pin = 15e3       # input power (W), changing this changes thrust but not Isp
Vd = 500.0       # discharge voltage (V)
L_ch = 0.051     # channel length (m)
d = 0.324        # diameter (m)
h = 0.058        # channel height (m)
A_ch = math.pi * d * h
T_neutral = 800.0  # neutral temperature (K)

# -------------------------
# Propellant Table
# -------------------------
species = OrderedDict([
    ("I2",  {"mass_amu": 2*126.90447, "sigma": 8.00e-20}),
    ("Carbon macro", {"mass_amu":150, "sigma":7.00e-20}),
    ("Bi",  {"mass_amu": 208.98040,    "sigma": 8.50e-20}),
    ("Sn",  {"mass_amu": 118.710,      "sigma": 5.00e-20}),
    ("Na",  {"mass_amu": 22.98976928,  "sigma": 1.50e-20}),
    ("K",   {"mass_amu": 39.0983,      "sigma": 2.00e-20}),
    ("H2O", {"mass_amu": 18.01528,     "sigma": 1.50e-20}),
    ("H_water", {"mass_amu": 2, "sigma":1.05e-20}),
    ("O_water", {"mass_amu": 32, "sigma":1.36e-20}),
    ("Ar",  {"mass_amu": 39.948,       "sigma": 2.50e-20}),
    ("Kr",  {"mass_amu": 83.798,       "sigma": 4.00e-20}),
    ("Xe",  {"mass_amu": 131.293,      "sigma": 6.00e-20}),
    ("Fe",  {"mass_amu": 55.845,       "sigma": 4.00e-20}),
])

# -------------------------
# Step 1: Discharge Current
# -------------------------
Id = Pin / Vd   # [A]

# -------------------------
# Helper Functions
# -------------------------
def neutral_thermal_speed(mass_amu, T):
    m_n = mass_amu * amu_kg
    return math.sqrt((8.0 * k_B * T) / (pi * m_n))

def gamma_model(mass_amu):
    m_i = mass_amu * amu_kg
    return 0.05 * math.sqrt((m_i * 0.05) / m_e)
N_eff = 1000   # effective electron pass multiplier
def mass_utilization_eta(Id, sigma_iz, u_n, Lch, Ach, gamma):
    exponent = - (Id / q_e) * (sigma_iz / u_n) * (Lch / Ach) * gamma* N_eff
    return 1.0 - math.exp(exponent)
m_i_d= {}
for name, props in species.items():
    mass_amu = props["mass_amu"]

    m_i_d[name] = mass_amu * amu_kg
    print(m_i_d[name])


# -----------------------------------
# Self-consistent solution for N_eff, eta_m, and mdot
# -----------------------------------

# Precompute per-species neutral speeds and gammas
u_n_dict = {}
gamma_vals = {}
for name, props in species.items():
    mass_amu = props["mass_amu"]
    u_n_dict[name] = neutral_thermal_speed(mass_amu, T_neutral)
    gamma_vals[name] = gamma_model(mass_amu)

# Initial guesses
N_eff_dict = {}
eta_m = {}
for name in species:
    N_eff_dict[name] = 100.0   # initial guess
    eta_m[name] = 0.5          # seed value

# Iterate to converge N_eff → ηm → mdot → n_n → N_eff
for iteration in range(15):

    # 1) Compute ηm using current N_eff_dict
    for name, props in species.items():
        sigma = props["sigma"]
        eta_m[name] = mass_utilization_eta(
            Id,
            sigma,
            u_n_dict[name],
            L_ch,
            A_ch,
            gamma_vals[name] * N_eff_dict[name]   # only change here
        )

    # 2) Compute mdot from ηm
    mdot = {}
    for name, props in species.items():
        m_i = props["mass_amu"] * amu_kg
        I_i_val = eta_m[name] * Id
        mdot[name] = I_i_val * m_i / q_e

    # 3) Compute new neutral density n_n
    n_n = {}
    for name, props in species.items():
        m_i = props["mass_amu"] * amu_kg
        n_n[name] = mdot[name] / (m_i * u_n_dict[name] * A_ch)

    # 4) Update N_eff based on mean free path
    for name, props in species.items():
        sigma = props["sigma"]
        if n_n[name] > 0:
            lambda_mfp = 1.0 / (n_n[name] * sigma)
        else:
            lambda_mfp = 1e12

        P_iz = L_ch / (L_ch + lambda_mfp)
        P_iz = max(P_iz, 1e-12)
        N_eff_dict[name] = 1.0 / P_iz

# Replace your scalar N_eff with per-species dictionary
N_eff = N_eff_dict

# Print results for confirmation
for name in species:
    print("η_m for", [name], eta_m[name])
    print("mdot for", [name], mdot[name])
    print("N_eff for", [name], N_eff[name])

# -------------------------
# Step 5a: Fixed Efficiency Terms
# -------------------------
eta_q = {}
eta_v = {}
eta_d = {}
eta_c = {}
eta_e = {}


for name in species:
    eta_q[name] = 0.9   # Charge utilization efficiency (fixed)
    eta_v[name] = 0.9   # Voltage utilization efficiency (fixed)
    eta_d[name] = 0.82   # Divergence efficiency (fixed assuming a divergence angle of 25 degrees)
    eta_c[name] = 0.93   # Cathode efficiency (fixed)
    eta_e[name] = 0.95   # Electrical efficiency (fixed)

# -------------------------
# Step 5b: Beam Efficiency η_b
# -------------------------

# Fixed beam-loss model constants
delta = 0.1       # sheath / divergence factor
alpha = 0.05      # wall loss factor
T_e = 800.0       # electron temperature [K]

# Electron thermal speed (at 800 K)
v_e = math.sqrt((8.0 * k_B * T_e) / (pi * m_e))

# Wall area estimate (cylindrical channel walls)
A_wall = math.pi * d * L_ch

# -------------------------
# Ionization Energy Model ε_iz
# -------------------------

# First ionization energies from your table (eV)
I_eV = {
    "I2": 10.45,
    "Carbon macro": 11.30,
    "Bi": 7.29,
    "Sn": 7.34,
    "Na": 5.14,
    "K": 4.34,
    "H2O": 12.60,
    "H_water": 13.60,
    "O_water": 13.60,
    "Ar": 15.76,
    "Kr": 14.00,
    "Xe": 12.13,
    "Fe": 7.90
}

# Literature mean energy per ion pair W (eV) for noble gases
W_literature = {
    "Xe": 21.9,
    "Kr": 23.6,
    "Ar": 26.3
}

# Fallback scaling factor for non-noble species
kappa_W = 2.5

# Energy cost per ion (J)
epsilon_iz = {}

for name in species:
    if name in W_literature:
        W_eV = W_literature[name]
    else:
        W_eV = kappa_W * I_eV[name]

    epsilon_iz[name] = W_eV * q_e  # [J]


# -------------------------
# Beam Efficiency η_b
# -------------------------

# Fixed electron temperature
T_e_eV = 61.5
T_e_J = T_e_eV * q_e

# Electron thermal speed from kinetic energy
v_e = math.sqrt(2.0 * T_e_J / m_e)

# Magnetic field & neutral density
B_field = 0.02    # [T]

# Dictionary to store neutral densities
n_n_d = {}

for name, props in species.items():
    # Mass of ion for this species
    m_i_local = m_i_d[name]

    # Recompute neutral thermal speed for each species
    u_n_local = neutral_thermal_speed(props["mass_amu"], T_neutral)

    # Compute neutral number density
    n_n_d[name] = mdot[name] / (m_i_local * u_n_local * A_ch)



# Wall area
A_wall = math.pi * d * L_ch

eta_b = {}

for name, props in species.items():

    m_i = props["mass_amu"] * amu_kg
    V_b = eta_v[name] * Vd
    eps_iz = epsilon_iz[name]

    # -------------------------
    # Electron-neutral collision frequency
    # ν_en = n_n * σ_en * v_e
    # -------------------------
    sigma_en = props["sigma"]        # using ionization cross-section as estimate
    n_n = n_n_d[name]
    nu_en = n_n * sigma_en * v_e    # [1/s]

    # -------------------------
    # Electron cyclotron frequency
    # ω_ce = qB / m_e
    # -------------------------
    omega_ce = q_e * B_field / m_e  # [rad/s]

    # -------------------------
    # Magnetization scaling (ν/ω)^2
    # -------------------------
    if omega_ce > 0:
        mag_scale = (nu_en / omega_ce)**2
    else:
        mag_scale = 0.0

    # -------------------------
    # Corrected, dimensionless numerator
    # -------------------------
    if V_b > 0:
        num = 1.0 - (0.5 * m_e * v_e**2 / (q_e * V_b)) * mag_scale
    else:
        num = 0.0

    # -------------------------
    # Denominator
    # -------------------------
    term_ionization = eps_iz / V_b if V_b > 0 else float('inf')
    term_wall = math.sqrt(m_i / m_e) * (delta**1.5) * alpha * (A_wall / A_ch)
    den = 1.0 + term_ionization + term_wall

    # -------------------------
    # Safe beam efficiency
    # -------------------------
    eta_raw = num / den if den != 0 else 0.0
    eta_b[name] = max(0.0, min(1.0, eta_raw))

# -------------------------
# Total Efficiency η_total
# -------------------------
eta_total = {}

for name in species:
    eta_total[name] = eta_q[name] * eta_v[name] * eta_d[name]*eta_e[name] * eta_c[name] * eta_b[name]*eta_m[name]
    print('The total efficiency for', [name], 'is', eta_total[name])


# -------------------------
# At this step we have a total efficiency that can be used to compute Thrust, Isp
# -------------------------

# -------------------------
# Exhaust velocity for each propellant
# -------------------------
v_ex= {}

for name in species:
    v_ex[name] = math.sqrt((2*eta_total[name]*Pin)/(mdot[name]))
    print('Effective exaust velocity for', [name], v_ex[name])

# -------------------------
# Momentum based thrust
# -------------------------
T_m= {}

for name in species:
    T_m[name] = mdot[name]*v_ex[name]
    print('momentum based thrust for', [name], 'is', T_m[name],'Newtons')

# -------------------------
# Power based thrust (same as momentum based, but wanted to double check)
# -------------------------
T_p= {}

for name in species:
    T_p[name]=math.sqrt(2*eta_total[name]*Pin*mdot[name])

# -------------------------
# Specific Impulse
# -------------------------
I_sp= {}

for name in species:
    I_sp[name]=v_ex[name]/g_0
    print('Specific Impulse for', [name], 'is', I_sp[name], 'seconds')



