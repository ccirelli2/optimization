# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 09:48:36 2020

@author: chris.cirelli

Ref: https://www.youtube.com/watch?v=iSnTtV6b0Gw
"""

# Load Python Libraries ------------------------------------------
import numpy as np
from scipy.optimize import minimize


# Define Function to calculate volume of box
def calcVolume(x):
    length = x[0]
    width = x[1]
    height = x[2]
    volume = length * width * height
    return volume

# Define Function to calculate surface area of box
def calcSurface(x):
    length = x[0]
    width = x[1]
    height = x[2]
    surfaceArea = 2*length*width + 2*length*height + 2*height*width
    return surfaceArea


# Define Objective Function for Optimization
''' This is the function that we are will try to minimize
    By minimizing the negative volume we will actually maximize the 
    volume of our box.
'''
def objective(x):
    return -1 * calcVolume(x)


# Define a function to return our constraints
'In this case we want our surface area to be euqal to or less than 10'
def constraint(x):
    return 10 - calcSurface(x)


# Scipy requires that constraints be loaded into a dictionary
cons = ({'type':'ineq', 'fun':constraint})

# Set Initial guess value for box dimensions
lengthGuess = 1
widthGuess = 1
HeightGuess = 1

# Load guess values into numpy array
x0 = np.array([lengthGuess, widthGuess, HeightGuess])


# Call Scipy minimize to solve the objective function with constraints
'''SLSQP Solver.  This is one of the only solvers that can do constrained
   non-linear optimization.
   options: display results as finishes.
'''
sol = minimize(objective, x0, method='SLSQP', constraints=cons,
               options={'disp':True})


# Retrieve Box sizing and volume
xOpt = sol.x
volumeOpt = -sol.fun

# Calculate Surface Area with Optimized (just to double check)
surfaceAreaOpt = calcSurface(xOpt)

# Print Results
print('Sol.x result => {}'.format(sol.x))
print('Length => {}'.format(xOpt[0]))
print('Width => {}'.format(xOpt[1]))
print('Height => {}'.format(xOpt[2]))
print('Volume => {}'.format(volumeOpt))
print('Surface Area => {}'.format(surfaceAreaOpt))










