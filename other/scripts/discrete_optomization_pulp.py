"""
Desc    Tutorial discrete optimization with Pulp.

Source  https://towardsdatascience.com/linear-programming-and-discrete-optimization-with-python-using-pulp-449f3c5f6e99
Linear Optomization : they involve maximizing or minimizing a linear objective 
       function, subject to a set of linear inequality or equality constraints

"""

from pulp import *
import cbcpy as cbc
solver1 = cbc.OsiClpSolverInterface()
solver1.readMps()




