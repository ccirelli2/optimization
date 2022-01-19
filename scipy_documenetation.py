# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 18:02:28 2020
@author: chris.cirelli

Ref : https://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html#optimization-scipy-optimize
"""

# Import Libraries ------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize


def rosen(x):
    """The Rosenbrock function"""
    return sum(100.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)

x0 = np.array([2, 3, 4, 5])

solution = minimize(rosen, x0, method='nelder-mead', options={'xatol':1e-8,
                                                              'disp':True})


def bruteforce(rosen):
    rosen_vals = []
    labels = []
    for x in range(0, 100000):
        x = np.random.randint(-10, 10, size=4)
        y = rosen(x)
        labels.append(sum(x))
        rosen_vals.append(y)
    df = pd.DataFrame({})
    df['y'] = rosen_vals
    df['label'] = labels
    df.sort_values(by='y', ascending=False, inplace=True)
    return df


test = bruteforce(rosen)

print(test)

    
    
    






