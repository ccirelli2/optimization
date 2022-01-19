# -*- coding: utf-8 -*-
"""
Ref : http://benalexkeen.com/linear-programming-with-python-and-pulp-part-1/
"""

###############################################################################
# Import Libraries
###############################################################################
import matplotlib.pyplot as plt
import numpy as np
import pulp 


###############################################################################
# Problem
###############################################################################
"""
Maximize :  Z = 4x + 3y
s.e.     :  x >= 0
            y >= 2
            2y <= 25 - x
            4y >= 2x - 8
            y <= 2x -5
"""

###############################################################################
# Plot Feesibility Region
###############################################################################

def plot_feesibility_region():
    # Construct Lines
    # x > 0
    x = np.linspace(0, 20, 2000)
    # y >= 2
    y1 = (x*0) + 2
    # 2y <= 25 - x
    y2 = (25-x) / 2.0
    # 4y >= 2*x - 8
    y3 = ((2*x) -8)/4.0
    # y <= 2*x-5
    y4 = 2*x-5
    
    # Construct Plot
    plt.plot(x, y1, label='x>0')
    plt.plot(x, y2, label='y>=2')
    plt.plot(x, y3, label='4y >= 2*x-8')
    plt.plot(x, y4, label='y <= 2*x-5')
    plt.xlim((0, 16))
    plt.ylim((0, 11))
    
    # Fill Feesibility Region
    y5 = np.minimum(y2, y4)
    y6 = np.maximum(y1, y3)
    plt.fill_between(x, y5, y6, where=y5>y6, color='grey', alpha=0.5)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

plot_feesibility_region()


def example1(pprint=True):
    # Instantiate Problem Class
    my_lp_problem = pulp.LpProblem("My LP Problem", pulp.LpMaximize)
    # Create X & Y Variables
    x = pulp.LpVariable('x', lowBound=0, cat='Continuous')
    y = pulp.LpVariable('y', lowBound=2, cat='Continuous')
    'The objective function and constraints are added using the += operator to our model.'
    # Add Objective Function
    my_lp_problem += 4 * x + 3 * y, "Z"
    # Add Constraints
    my_lp_problem += 2*y <= 25 - x
    my_lp_problem += 4*y >= 2*x - 8
    my_lp_problem += y <= 2*x-5
    # Show Model
    if pprint:
        print(my_lp_problem)
    # Solve
    my_lp_problem.solve()
    status = pulp.LpStatus[my_lp_problem.status]
    print(status)
    # Get Results
    for variable in my_lp_problem.variables():
        print("{} = {}".format(variable.name, variable.varValue))
    print(pulp.value(my_lp_problem.objective))


#example1(pprint=False)





















