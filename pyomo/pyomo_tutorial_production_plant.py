# -*- coding: utf-8 -*-
"""
Ref : https://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/02.01-Production-Models-with-Linear-Constraints.ipynb

Problem :
    Suppose you are thinking about starting up a business to produce Product X.
    You have determined there is a market for X of up to 40 units per week
    at a price of USD 270 each. 
    The production of each unit requires USD 100 of raw materials,
    1 hour of type A labor, and 2 hours of type B labor.
    You have an unlimited amount of raw material available to you, but only 80 hours per 
    week of labor A at a cost of USD 50/hour, and 100 hours per week of labor B at a cost of USD 40 
    per hour. Ignoring all other expenses, what is the maximum weekly profit?

Variables :
    Product = X
    Market = 40 units per week
    Price = 240
    Cost = 100 per unit
    Labor Types = A & B
    Labor_cost = Each unit, 1hr type A & 2hrs type B
    Time = 80 hours labor A per week @ $50 per hour
           100 hours of labor B per week @ 40 per hour.

Optimization Problem :
    What is the maximum weekly profit?

"""


price = 240
materials = 100
cost_laborA = 50
# cost to build 1 unit with labor B = 2*40 or 80 dollars
# cost to build 1 unit with labor A = 1*50 or 50 dollars



# Import Libraries ------------------------------------------------------------
from pyomo.environ import *


# Pyomo Model -----------------------------------------------------------------
def production():
    ''' Notes :
        - The way that variable model.x is being used it almost appears as if
        we have created a generic data type to be used throughout the funct
        as opposed to defining a single variable that we use in a single
        instance.
        - It is not quite clear how the constraints work as they are not
        linked to a cost.
        - The objective function isn't quite clear.  Are we saying here that
        we need to maximize 40 * some real number?
    '''
    # Instantiate Model
    model = ConcreteModel()
    # Declare Decision Variable (In this case it looks like the num units produced)
    model.x = Var(domain=NonNegativeReals)
    # Declare Objective Function
    model.profit = Objective(expr = 40*model.x, sense=maximize)
    # Declare Constraints
    model.demand = Constraint(expr = model.x <= 40)
    model.laborA = Constraint(expr = model.x <= 80)
    model.laborB = Constraint(expr = 2*model.x <= 100)
    # Solve the Model
    solver = SolverFactory('glpk')
    results = solver.solve(model)
    results.write(num=1)
    model.solutions.store_to(results)
    print(results.solution)
    # Get Profit and Units Per Week
    print("Profit = ", model.profit(), " per week")
    print("X = ", model.x(), " units per week")

production()