# -*- coding: utf-8 -*-
"""
Ref: http://benalexkeen.com/linear-programming-with-python-and-pulp-part-3/
"""

# Import Modules
import pulp
import numpy as np


# Problem Statement
""" Problem : Maximize car production profit
    Profit = 30,000A + 45,000B
    s.e.
            A >= 0
            B >= 0
            3A + 4B <= 30    #Days.  Production restricted to one month.
            5A + 6B <= 60    # Engineer time restriction
            1.5A + 3B <= 21  # Detailer time restriction

"""

# Instantiate Model
model = pulp.LpProblem("Profit_maximisation_problem", pulp.LpMaximize)

# Define Decision Variables
A = pulp.LpVariable('A', lowBound=0, cat='Integer')
B = pulp.LpVariable('B', lowBound=0, cat='Integer')

# Objective Function
model += 30000*A + 45000*B, 'Profit'

# Constraints
model += 3 * A + 4 * B <= 30
model += 5 * A + 6 * B <= 60
model += 1.5 * A + 3 * B <= 21

# Solve our problem
model.solve()
print(pulp.LpStatus[model.status])

# Print our decision variable values
print("Production of Car A = {}".format(A.varValue))
print("Production of Car B = {}".format(B.varValue))


# Print Model Profit value versus original without optimization
print('Model profit vs non-model profit = {} vs {}'.format(
    pulp.value(model.objective), '300,000'))

