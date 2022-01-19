# -*- coding: utf-8 -*-
"""
Description:  Chapter 1 of Optomization with Pyomo book

References: 
    http://www.pyomo.org/
    https://pyomo.readthedocs.io/en/stable/pyomo_overview/simple_examples.html

Created on Sun Jul 19 10:31:39 2020
@author: chris.cirelli
"""

# Import Libraries ------------------------------------------------------------
from __future__ import division  # ensure that values are converted to floats

from pyomo.environ import *

# Abstract Model Example ------------------------------------------------------
model = AbstractModel()          # Call model

# Declare Parameters usin Param function --------------------------------------
''' We pass the within value to Param in order to define what are the
    acceptable values that the function can accept.  Here, any value that is
    negative will throw an error.
'''
model.m = Param(within=NonNegativeIntegers)
model.n = Param(within=NonNegativeIntegers)

# Defining an Index -----------------------------------------------------------
''' The index will define the possible range of values that the function will
    accept and or utilize.
'''
model.I = RangeSet(1, model.m)
model.J = RangeSet(1, model.n)

# Not clear
model.a = Param(model.I, model.J)
model.b = Param(model.I)
model.c = Param(model.J)


# Declare a variable x that is indexed by the set J ---------------------------
model.x = Var(model.J, domain=NonNegativeReals)


# Passing Functions to Pyomo --------------------------------------------------
'''  Here we are creating a function that will be passed to pyomo. Summation
     is a native function of pyomo.  Within it we pass model.c and model.x that
     will be summed over their indexes.
'''
def obj_expression(model):
    return summation(model.c, model.x)


# Declare and Object Function -------------------------------------------------
'''Use Objective() function.
The default pyomo objective function is minimization.  To maximize we pass
sense=maximize.
the rule= argument is given the name of a function that returns the exp
to be used.
'''
model.Obj = Objective(rule=obj_expression)


# Declaring Constraints -------------------------------------------------------
''' There is a similar process to defining constraints.  We declare a constraint
    function that is passed to pyomo.   
    Here, we define the constraint for every i in the index. 
'''

def ax_constraint_rule(model, i):
    i.constraint = sum(model.a[i, j] * model.x[j] for j in model.J) >= model.b[i]
    
    
# Passing Constraints to Pyomo ------------------------------------------------
''' Create one constraint for each member  of the set model model.I
'''
model.AxbConstraint = Constraint(model.I, rule=ax_constraint_rule)


# Passing Data to the Model ---------------------------------------------------
''' statements must be terminated with a semi-colon. 
'''
param m := 1;










































          