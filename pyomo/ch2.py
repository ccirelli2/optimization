# -*- coding: utf-8 -*-
"""
Chapter 2 : Introduction to Mathematical Modeling
"""

# Import Pyomo Modules --------------------------------------------------------
from pyomo.environ import *


# 2.1.1 Overview
'''
Concepts :
    Variables - Unknown or changing parts of a model, e.g. which decisions to
    take, or the characteristics of a system of outcomes.
    Parameters - These are symbolic representations of real world data.
    Relations - These are equations, inequalities, or other mathematical
    relationships that define how different parts of a model are related
    to each other.
Ex : 
    Problem - A person wants to determine the optimal number of scoops of
    ice-cream to buy.
    x = number of scoops
    c = cost per scoop
    cx = total cost of n scoops
Mathematical Notation :
    Total cost can be represented in simpler notation 
    Sigma ci*xi for i...n

    xi >=0, i { A
    x subscript i is greater or equal to 0 for all i in A.
'''


# 2.2 Optimization
'''
Symbol x :
    x is often used as a variable in optimization modeling.  It is sometimes
    called the decision variable because we use optimizaiton models to
    help make better decisions. 'x' is not used to denote data.

Symbol c :
    Often are used to refer to data or parameters.  An example is cost.

Objective Function :
    Objective to perform the optimization. Optimization results in the best
    or optimal value of the objective function.

Decision Variables :
    in the icecream scoop example, 'x' would be the number of scoops as it
    is the decision variable that we are focused on, looking for a solution
    to.
'''

# Linear & Non-Linear Optimization Models
'''
Linear :
    An expression is optimization is said to be linear if it is composed
    only of sums of decision variables and or decision variables multiplied
    by data.
    We say that an expression is linear because the decision variables
    are only mutiplied by data and summed.

Objective Function :
    Should try to keep linear else conver to linear.
Constraints :
    According to the book,nonlinear objective functions are easier to
    solve then nonlinear constraints.
'''

# 2.4 Modeling With Pyomo
'''
Abstract Formulation :
'''

def abstract_v1():
    model = AbstractModel(name="H")
    model.A = Set()
    model.h = Param(model.A)
    model.d = Param(model.A)
    model.c = Param(model.A)
    model.b = Param()
    model.u = Param(model.A)

    def xbounds_rule(model, i):
        return (0, model.u[i])
    model.x = Var(model.A, bounds=xbounds_rule)

    def obj_rule(model):
        return sum(model.h[i] * (model.x[i] - (model.x[i]/model.d[i])**2)
                   for i in model.A)
    model.z = Objective(rule=obj_rule, sense=maximize)
    def budget_rule(model):
        return sum(model.c[i]*model.x[i] for i in model.A) <= model.b
    model.budgetconstr = Constraint(rule=budget_rule)

# Solving Pyomo Models
'''
Pyomo does not solve the problem, but sends the data and equations to a solver.
'''



















