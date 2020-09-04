# -*- coding: utf-8 -*-
"""
Chapter 3 - Pyomo Overview
"""

# Import Libraries
from pyomo.environ import *


# 3.1 Introduction
'''
Modeling Components :
    1.) Var  optimization variables in model
    2.) Objective  expressions that are minimized or maximized
    3.) Constraint  constraint expression in a model
    4.) Set  set data that is used to define a model instance
    5.) Param  parameter data that is used to define a model instance

This chapter provides an overview of these components and how to define and
solve a Pyomo model.
'''


# 3.2 Warehouse Location Problem
'''
Problem : Considers the optimal location for warehouses to meet demand.
          We wish to determine the optimal warehouse location that will
          minimize the overall cost of delivery.
          
Variables :
    N       number of candidate warehouse location.
    M       be a set of customer locations.
    d n,m   for each warehouse 'n', the cost to deliver a product to
            customer 'm'
    yn      Variable that specifies whether a warehouse should be built, where
            yn is 1 if warehouse n is selected and 0 if not.
   x n,m    represents the fraction of demand for customer m that is served by
            warehouse n.
   P        Total number fo warehouses that can be built.
Optimizer :
    Determines the values for x & y and all other variables are known
    input parameters to the model.
'''


# 3.3.1 Components for Variables, Objectives & Constraints
'''
Requirements :
    Optimization at minimum requires one variable and an objective function.
    Most problems include constraints.
    Pyomo classes for implementing these concepts are Var, Objective,
    Constraint.
'''

def concrete_v1():
    model = ConcreteModel()
    solver = SolverFactory('glpk')
    model.x = Var()
    model.y = Var(bounds=(-2, 4))
    model.z = Var(initialize=1.0, within=NonNegativeReals)
    model.obj = Objective(expr= model.x*2 + model.y + model.z,
                          sense=maximize)
    model.eq_con = Constraint(expr= model.x + model.y + model.z == 1)
    model.ineq_con = Constraint(expr = model.x + model.y <= 0)
    results = solver.solve(model)
    results.write()
    model.solutions.store_to(results)
    print(results.solution)

''' 
Explanation

1.) In this example we have created three optimization variables (x, y, z)
2.) A single objective function model.obj
3.) And two constraints eq_con and ineq_con
4.) This example defines variable "x" to be a continuous variable (by default?)
    We can use initialize, within and bounds to set specifications for the
    variables.
'''


# 3.3.2 Indexed Components
'''
Variables : In the previous example each Var() was a scalar.
            The constraints were also scalars.  Ex == 1 or <=0
Indexed Components : When working with large complex models it is common
    to have vectors of variables and constraints whose dimension and indexing
    is determined according to model data (?).

Example :
    N = [’Harlingen’, ’Memphis’, ’Ashland’]
    M = [’NYC’, ’LA’, ’Chicago’, ’Houston’]
    model.x = Var(N, M, bounds=(0,1))
    model.y = Var(N, within=Binary)

    Note that variable "N" is indexed by N and M, which is a two dimensional
    array.  Values can be accessed by x[ij] notation.
    Variable N is indexed by "N" or i in matrix notation.
    Redefining Constraint :
        v1 = Constraint(expr = model.x + model.y <=0)
        v2 = Constraint(expr = sum(model.y[n] for n in N) <=P))
        For v2, the sum over all y values must be less or equal to P, which is
        the capacity constraint.
    Note : We would use a similar constraint to create the rate neutral
    constraint for our model.

    Redefined Objective Function
    model.obj = Objective(expr = sum(d[n,m] * model.x[n,m]
                                     for n in N for m in M))
'''



# 3.3.3 Construction Rules
'''
Purpose : Apply a constraint to each value of an object
How :     Write a user defined function that is then passed as a constraint
          to the constraint class.

Example :
    def one_per_cust_rule(model, m):
        return sum(model.x[n, m] for n in N) ==1
    model.one_per_cust = Constraint(M, rule=one_per_cust_rule)
    
    (model, m) : we pass in both the model and the index variable
    return : for every n in model.x it must meet the constraint of ==1
    constraint : create a constraint by lassing a "rule" that is the name
    of the function that we created.  The constraint is indexed by M.

    When Pyomo constructs the Constraint object, the construction rule is
    called for each of the values of the specified index sets.

NOTE: Pyomo expects a construction rule to return an expression for every
    index value. If no constraint is needed for a particular combination of indices,
    then the value Constraint.Skip can be returned instead.

Important : Construction Rules & Expected Type Returns
    Set : A python set or list
    Param : An integer or float
    Object : An Expression
    Constraint : A constraint expression
'''

# 3.3.4 Abstract & Concrete Models
'''
1.) Concrete Models
    - Immediately construct model components.
    - *A concrete model can be used when data is available before model
      components are declared.
2.) Abstract Models
    - Defer component construction
    
'''

# 3.35 Concrete Model for Warehouse Location

def warehouse_concrete_model(display):
    # Instantiate Model
    model = ConcreteModel(name="WL")
    # Create Data
    N = ['Harlingen', 'Memphis', 'Ashland']
    M = ['NYC', 'LA', 'Chicago', 'Houston']
    d = {('Harlingen', 'NYC'): 1956,
         ('Harlingen', 'LA'): 1606,
         ('Harlingen', 'Chicago'): 1410,
         ('Harlingen', 'Houston'): 330,
         ('Memphis', 'NYC'): 1096,
         ('Memphis', 'LA'): 1792,
         ('Memphis', 'Chicago'): 531,
         ('Memphis', 'Houston'): 567,
         ('Ashland', 'NYC'): 485,
         ('Ashland', 'LA'): 2322,
         ('Ashland', 'Chicago'): 324,
         ('Ashland', 'Houston'): 1236
         }
    P = 2
    # Declare Variables (x = NM matrix)
    model.x = Var(N, M, bounds=(0,1))
    if display:
        print('Var "x" ', model.x.display())
    model.y = Var(N, within=Binary)
    if display:
        print('Var "y"', model.y.display())
    if display:
        print('Dict "d"', d)
    # Define Objective Rule
    def obj_rule(model):
        return sum(d[n, m] * model.x[n, m] for n in N for m in M)
    model.obj = Objective(rule=obj_rule)
    # Define Customer Constraint
    def one_per_cust_rule(model, m):    
        return sum(model.x[n, m] for n in N) == 1
    model.one_per_cust = Constraint(M, rule=one_per_cust_rule)
    # Warehouse Active Rule
    def warehouse_active_rule(model, n, m):
        return model.x[n, m] <= model.y[n]
    model.warehouse_active = Constraint(N, M, rule=warehouse_active_rule)
    # Num Warehouses Rule
    def num_warehouses_rule(model):
        return sum(model.y[n] for n in N) <= P
    model.num_warehouses = Constraint(rule=num_warehouses_rule)



# 3.3.3 Importing Data
'''
The book uses an example whereby they import data via a pandas dataframe.
They then define each variable as a list.
Ex :
    N = list(df.index.map(str))
    M = list(df.columns.map(str))

They then create Pyomo variables indexed by these same lists.
model.x = Var(N, bounds=(1,0))
model.y = Var(M, within=Binary)
'''


# 3.3.6 Modeling Components For Sets and Parameters
'''
Sets :
    - is used to declare valid indices for any component that is indexed.
    - These set objects can be used to define indexed variables or constraints
    Ex :
        model.N = Set()
        model.M = Set()
        model.x = Var(model.N, model.M, bounds=(1,0))
        model.y = Var(model.N, within=Binary)
    We first create two set objects.
    W/r/t model.x we create a 2D array indexed by N and M with bounds 1,0.
    So, essentially, this is a matrix

'''
def ex_create_var_indexed_by_set():
    model = ConcreteModel()
    N = Set(initialize=range(4))
    M = Set(initialize=range(4))
    model.x = Var(M, N, bounds=(0,1))  # notice how this becomes a matrix
    model.y = Var(N, within=Binary) # notice how this is a single array
    model.x.display()
    model.y.display()
    
    # Pyomo set objects can be indexed by other sets
    model.z = Set(M)
    model.z.display() # doesn't really specify the index values.


# Pyomo Parameter Component
'''
Param :
    Used to define data values for a problem.
    Ex :
        model.d = Param(model.N, model.M)
        model.P = Param()
        This example declares a scalar parameter P and
        an indexed parameter d.
    *By default, parameters are immutable.  Once the values are set they
    cannot be changed.
'''
def param_ex():
    model = ConcreteModel()
    N = Set(initialize=range(4))
    M = Set(initialize=range(4))
    model.d = Param(N, M)
    model.x = Var(N, bounds=(0,1))
    
    model.d.display()


param_ex()


































