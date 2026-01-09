"""
Created on Sun Nov 23 16:47:24 2025

@author: joahb
this is used to solve for x after running throughe PR_EOS sheet
this is what you do to find the final temp of a throttling process given initial temp
pressure

1) make sure the properties of the fluid are setup correctly in 'props' (critical temps and heat capacity)
2) enter the initial temp and pressure under "current state" and note the enthalpy at the bottom of "H" column
3) enter the final pressure and iterate the final temp until you get a fugacity ratio as close as possible to 1
4) H_v is the first number in "H" column and H_l is the last
5) enter the values here
"""

import sympy as sp

# Define symbol
x = sp.symbols('x')
'''
# initial enthalpy
H_in = -7452.51

#Final enthalpies for liquid and vapor
H_v = -6438.789751
H_l = -1.176771925e4
'''
# initial enthalpy
H_in = -7452.50581206115

#Final enthalpies for liquid and vapor
H_v = -6445.24354084509
H_l = -11779.2734867917

# Define the equation H_in = x*H_v + (1-x)*H_l
equation = sp.Eq(H_in, x*H_v + (1 - x)*H_l)

# Solve for x
solution = sp.solve(equation, x)

print('The quality of this mixture is', solution[0])
liquid_yeild= 1-solution[0]

print('The liquid yield of this throttling process is:', liquid_yeild)

