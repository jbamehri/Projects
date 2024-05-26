# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 23:37:54 2024

@author: joahb
"""

import numpy as np
import matplotlib.pyplot as plt

# Constants
G_MARS = 3.72076  # Mars surface gravity in m/s^2
MASS_ROVER_EARTH = 1982/2.205  # Mass of the rover in kg on Earth
MASS_ROVER_MARS = 743/2.205  # Mass of the rover in kg on Mars
DRAG_COEFFICIENT = 0.8  # Approximate drag coefficient for a streamlined object like a rover
SURFACE_AREA = 20  # Surface area of the rover in m^2
TIME_STEP = 0.1  # Time step for simulation in seconds

# Default input parameters
DEFAULT_TEMPERATURE = 243.94331  # Temperature in Kelvin
DEFAULT_WIND_COMPONENT = -1.245691  # W-E wind component in m/s
DEFAULT_DENSITY = 0.015058827  # Density in kg/m^3
DEFAULT_DUST_DEPOSITION_RATE = 4.658803e-10  # Dust deposition rate in kg/m^2/s

# Function to get input conditions from the user
def get_input_conditions():
    temperature_input = input(f"Enter temperature (default: {DEFAULT_TEMPERATURE}): ")
    temperature = float(temperature_input) if temperature_input else DEFAULT_TEMPERATURE

    wind_input = input(f"Enter W-E wind component in m/s (default: {DEFAULT_WIND_COMPONENT}): ")
    wind_component = float(wind_input) if wind_input else DEFAULT_WIND_COMPONENT

    density_input = input(f"Enter density in kg/m^3 (default: {DEFAULT_DENSITY}): ")
    density = float(density_input) if density_input else DEFAULT_DENSITY

    dust_input = input(f"Enter dust deposition rate in kg/m^2/s (default: {DEFAULT_DUST_DEPOSITION_RATE}): ")
    dust_deposition_rate = float(dust_input) if dust_input else DEFAULT_DUST_DEPOSITION_RATE

    return temperature, wind_component, density, dust_deposition_rate

# Function to calculate drag force
def calculate_drag_force(velocity, density):
    return 0.5 * density * velocity**2 * DRAG_COEFFICIENT * SURFACE_AREA

# Function to calculate acceleration due to drag
def calculate_drag_acceleration(velocity, density):
    drag_force = calculate_drag_force(velocity, density)
    return -drag_force / MASS_ROVER_MARS  # Using mass on Mars for acceleration calculation

# Function to simulate descent and landing
def simulate_descent(temperature, wind_component, density, dust_deposition_rate, reactivity_factor):
    time = 0
    velocity = 0
    position = 1000  # Starting altitude in meters
    altitude = [position]
    time_values = [time]

    while position > 0:
        # Calculate air density based on temperature
        air_density = DEFAULT_DENSITY * (temperature / DEFAULT_TEMPERATURE)

        # Calculate gravitational force
        gravity_force = G_MARS * MASS_ROVER_MARS

        # Calculate drag force and acceleration
        drag_acceleration = calculate_drag_acceleration(velocity, air_density)

        # Update velocity and position
        velocity += (gravity_force + drag_acceleration) * TIME_STEP
        position -= velocity * TIME_STEP

        # Update time
        time += TIME_STEP

        # Adjust position for wind with reactivity factor
        position -= wind_component * TIME_STEP * (1 + reactivity_factor * (wind_component - DEFAULT_WIND_COMPONENT))

        # Adjust position for dust deposition with reactivity factor
        position -= dust_deposition_rate * TIME_STEP * (1 + reactivity_factor * (dust_deposition_rate - DEFAULT_DUST_DEPOSITION_RATE))

        altitude.append(position)
        time_values.append(time)

    return time_values, altitude

# Function to plot the simulations
def plot_simulations(reactivity_factor):
    # Get user input conditions
    temperature, wind_component, density, dust_deposition_rate = get_input_conditions()

    # Get default simulation
    default_simulation = simulate_descent(DEFAULT_TEMPERATURE, DEFAULT_WIND_COMPONENT, DEFAULT_DENSITY, DEFAULT_DUST_DEPOSITION_RATE, reactivity_factor)

    # Plot default simulation
    plt.plot(default_simulation[0], default_simulation[1], label='Default Parameters')

    # Plot simulations with parameter changes
    user_simulation = simulate_descent(temperature, wind_component, density, dust_deposition_rate, reactivity_factor)
    plt.plot(user_simulation[0], user_simulation[1], label='User Input')

    plt.title(f'Descent and Landing of Rover on Mars with Reactivity Factor {reactivity_factor}')
    plt.xlabel('Time (s)')
    plt.ylabel('Altitude (m)')
    plt.grid(True)
    plt.legend()
    plt.show()

    # Calculate RMSE
    default_altitude = np.array(default_simulation[1])
    user_altitude = np.array(user_simulation[1])


    # Pad the shorter array with NaN values to match the length of the longer array
    max_length = max(len(default_altitude), len(user_altitude))
    default_altitude = np.pad(default_altitude, (0, max_length - len(default_altitude)), mode='constant', constant_values=np.nan)
    user_altitude = np.pad(user_altitude, (0, max_length - len(user_altitude)), mode='constant', constant_values=np.nan)

    rmse = np.sqrt(np.nanmean((user_altitude - default_altitude) ** 2))
    print(f"RMSE between user input and default parameters: {rmse:.2f} meters")
   

# Get user input for reactivity factor
reactivity_factor = float(input("Enter reactivity factor: "))
plot_simulations(reactivity_factor)