# -*- coding: utf-8 -*-
"""
Pyomo : Python Optimization Modeling Objects Software

Ref : http://www.pyomo.org/
      https://github.com/Pyomo/pyomo

All Book Code Examples : pyomo/examples/doc/pyomobook
    https://jckantor.github.io/ND-Pyomo-Cookbook/

Optimizers
    IPOPT : Used for non-linear optimization
    GLPK : Used for linear optimization and solutions in this book.
    CPLEX : For Stochastic optimization.
"""

# Import Library --------------------------------------------------------------
from pyomo.environ import *


# 1.2 A Simple Example --------------------------------------------------------
'''
min x1 + 2x2
st 3x1 + 4x2 >=1
   2x1 + 5x2 >=2
   x1, x2 >=0

Model Components :
Model components are objects that are attributes of a model object, and the
ConcreteModel object initializes each model component as they are added. The
model decision variables, constraints, and objective are defined using Pyomo model
components.
'''

def concrete_model_v1():
    # Instantiate Model
    model = ConcreteModel()
    # Import Solver
    solver = SolverFactory('glpk')
    # Define Variables for the model (these are single values, not sets)
    model.x_1 = Var(within=NonNegativeReals)
    model.x_2 = Var(within=NonNegativeReals)
    # Define Objective Expression - Minimize (x1 + 2 * x2)
    model.obj = Objective(expr=model.x_1 + 2*model.x_2, sense=minimize)
    # Define Constraints - Determines what values x1 and x2 can take
    model.con1 = Constraint(expr= 3 * model.x_1 + 4 * model.x_2 >= 1)
    model.con2 = Constraint(expr= 2 * model.x_1 + 5 * model.x_2 >=2)
    # Solve Function
    results = solver.solve(model)
    # Print Model Results
    results.write(num=1)
    model.solutions.store_to(results)
    print(results.solution)
    # Print Objective Function & Each Variable
    print('Objective Function Solution => {}'.format(model.obj()))
    print('Optimal solution x1 => {}'.format(model.x_1()))
    print('Optimal solution x_2 => {}'.format(model.x_2()))
concrete_model_v1()


# 1.2.2 Minimum Graph Coloring Example ----------------------------------------
''' The graph coloring problem concerns the assignment of colors to vertices of
    a graph such that no two adjacent vertices share the same color.

    The objective in the minimum graph coloring problem is to find a valid
    coloring that uses the minimum number of distinct colors.
'''


