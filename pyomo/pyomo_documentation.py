# -*- coding: utf-8 -*-
"""
Questions:
    1. What is the difference between a parameter and a variable?
    2. Do all iterables need an index?
    


Ref : https://pyomo.readthedocs.io/en/stable/pyomo_overview/simple_examples.html

"""

# Import Libraries ------------------------------------------------------------
from __future__ import division  #converts values to floats before division
from pyomo.environ import *
import numpy as np

# Create Simple Abstract Model ------------------------------------------------
'''
Objective = min  sum(cjxj) from j=1 to n
s.t.      = sum(aijxj >= bi   for all i = 1...m)
            xj >= 0           for all j = 1...n)

Objective Functions
    To declare an objective function, the Pyomo function called Objective is
    used. The rule argument gives the name of a function that returns the
    expression to be used. The default sense is minimization. For maximization,
    the sense=maximize argument must be used. The name that is declared,
    which is OBJ in this case, appears in some reports and can be almost
    any name.

Input Data File
    Not clear at all.
'''

def simple_abstract_model():
    # Instantiate Model
    model = AbstractModel()
    # Create Abstract Parameters (Values not yet assigned)
    # restricts submitted values to non-negative integers
    model.m = Param(within=NonNegativeIntegers) 
    model.n = Param(within=NonNegativeIntegers)
    # Create Set Objects
    model.I =  RangeSet(1, model.m)  # these are the for all conditions
    model.J = RangeSet(1, model.n)
    # Create Parameters from Range Objects
    model.a = Param(model.I, model.J)
    model.b = Param(model.I)
    model.c = Param(model.J)
    # Declare a Variable 'x' Indexed by the set J
    model.x = Var(model.J, domain=NonNegativeReals)
    # Define Objective Function
    def obj_expression(model):
        '''
        returns an expression for the sum of the product of the two arguments 
        over their indexes.'''
        return summation(model.c, model.x)
    model.OBJ = Objective(rule=obj_expression)
    # Define Constraints
    def ax_constraint_rule(model, i):
        return sum(model.a[i, j] * model.x[j] for j in model.J) >= model.b[i]
    # Create Constraint for each member of set model.I
    model.AxbConstraint = Constraint(model.I, rule=ax_constraint_rule)


# Concrete Model
''' min 2x1 + 3x2
   s.t. 3x1 + 4x2 >= 1
   s.t. x1, x2 >=0
'''

def simple_concrete_model_v1():
    'expr : only available in concrete models'
    # Instantiate Concreate Model
    model = ConcreteModel()
    model.x = Var([1,2], domain=NonNegativeReals)
    model.OBJ = Objective(expr = 2*model.x[1] + 3*model.x[2])
    model.Constraint1 = Constraint(expr = 3*model.x[1] + 4*model.x[2] >=1)
    # solve the model and report the results
    solver = SolverFactory('glpk')
    results = solver.solve(model)
    # Print Model Structure
    #model.pprint()
    # Print Model Results
    results.write(num=1)
    model.solutions.store_to(results)
    print(results.solution)


def simple_concrete_model_v2():
    model = ConcreteModel()
    model.x_1 = Var(within=NonNegativeReals)
    model.x_2 = Var(within=NonNegativeReals)
    model.obj = Objective(expr=model.x_1 + 2*model.x_2)
    model.con1 = Constraint(expr=3*model.x_1 + 4*model.x_2 >= 1)
    model.con2 = Constraint(expr=2*model.x_1 + 5*model.x_2 >= 2)
    solver = SolverFactory('glpk')
    results = solver.solve(model)
    results.write()
    model.solutions.store_to(results)
    print(results.problem)




##########################    MODELING COMPONENTS    ##########################

# Sets ------------------------------------------------------------------------
'''Operations
    Declared using Set or RangeSet() functions
    model.A = Set()
    The Initialize option can accept any Python iterable
    model.D = Set(initialize=['red', 'green', 'blue'])
'''

def create_set_objects():
    model = ConcreteModel()
    # Create Set Using List
    model.A = Set(initialize=['red', 'green', 'blue'])
    # Create Set Using List Comprehension & Range
    model.B = Set(initialize=[x for x in range(0,10)])
    # Create Set Using Function
    def x_init(m):
        for i in range(10):
            yield 2*i+1
    model.C = Set(initialize=x_init)
    # Using RangeSet Function
    model.D = RangeSet(1.5, 10, 3.5)
    # Send Results to Stdout
    model.A.pprint()
    model.B.pprint()
    model.C.pprint()
    model.D.pprint()

# Pre-Defined Sets ------------------------------------------------------------
''' Pyomo provides a number of pre-defined or built in sets
    Example:
     set model.M is declared to be within the virtual set NegativeIntegers
     then an attempt to add anything other than a negative integer will result
     in an error.
'''
def create_predefined_set():
    model.M = Set(within=NegativeIntegers)
    model.M.pprint()


# Parameters ------------------------------------------------------------------
''' In pyomo, parameters refers to data that must be provided in order to find
    an optimal (or good) assignment of values to a decision variable.
'''

def create_parameters():
    model = ConcreteModel()
    model.X = RangeSet(1.5, 10, 3.5)
    model.Y = RangeSet(1.5, 10, 3.5)
    model.P = Param(model.X, model.Y)

# Variables -------------------------------------------------------------------
'''Variables are intended to ultimately be given values by an optimization
    package. They are declared and optionally bounded, given initial values,
    and documented using the Pyomo Var function.
    
    bounds = A function (or Python object) that gives a (lower,upper) bound
    pair for the variable
    domain = A set that is a super-set of the values the variable can take on.
    initialize = A function (or Python object) that gives a starting value for
    the variable; this       is particularly important for non-linear models
    within = (synonym for domain)
'''

def create_bounded_var():
    model = ConcreteModel()
    model.v1 = Var(within=NonNegativeIntegers, bounds = (0,6), initialize=1)
    model.v2 = Var(within=NonNegativeReals, bounds = (0,6), initialize=1.5)
    model.v1.pprint()
    model.v2.pprint()


# Objectives ------------------------------------------------------------------
''' An objective is a function of variables that returns a value that an
    optimization package attempts to maximize or minimize.
'''

def example_objective_funct():
    model = ConcreteModel()
    model.v1 = Var(within=NonNegativeIntegers, initialize=1, bounds=(1,6))
    model.v2 = Var(within=NonNegativeIntegers, initialize=1, bounds=(1,6))
    def obj_funct(model):
        return model.v1+model.v2
    model.Obj = Objective(rule=obj_funct, sense=maximize)
    model.con1 = Constraint(expr = model.v1 >= 1)
    model.con2 = Constraint(expr = model.v2 >=1)
    model.con3 = Constraint(expr = model.v1 <= 6)
    model.con4 = Constraint(expr = model.v2 <= 6)
    solver = SolverFactory('glpk')
    results = solver.solve(model)
    results.write()
    model.solutions.store_to(results)
    print(results)


def proj_test():
    # Instantiate Model
    model = ConcreteModel()
    # Create Random Numpy Arrays for Premiums & RMF
    model.prems = Set(initialize=np.random.randint(100, 1000, 100))
    model.rmf = Set(initialize=np.random.uniform(.9, 1.25, 100))
    model.add = Var(within=NonNegativeReals, bounds = (0, 0.5), initialize=.01)
    # Add Constraints
    model.con1 = Constraint(expr = model.rmf + model.add <= 1.25)
    # Define Objective Function
    def objective_expression(model):
        return summation(model.prems, model.rmf)
    model.Obj = Objective(rule=objective_expression, sense=maximize)


# Constraints -----------------------------------------------------------------
'''
'''

# Can be passed as a function
def f1():
    return (model.x['Index1'] + model.x['Index2'] == 3)

def ex_function_constraint():
    model.constr1 = Constraint(rule=f1)
    return model.constr1 

# Define Constraint Within a Tuple of Bounds (lb, expr, ub)
def aRule():
    model.x = Var()
    return (2, model.x, 4)

def aConstraint():
    model.aRule = Constraint(rule=aRule)
    return model.aRule

# Define Constraints With Index Variables
def model_w_indexed_constraint():
    model = ConcreteModel()
    model.A = RangeSet(1,10)
    model.a = Param(model.A, within=PositiveReals)
    model.toBuy = Var(model.A)
    def aRule(model, i):
        return model.a[i]*model.toBuy[i] <= i
    aBudget = Constraint(model.A, rule=aRule)



# Solving Pyomo Models --------------------------------------------------------

def solve_concrete_model():
    opt = pyo.SolverFactory('glpk')
    opt.solve(model)
    
def solve_abstract_model():
    instance = model_create_instance()
    opt = pyo.SolverFactory('glpk')
    opt.solve(instance)
    
    
    
# Accessing Object Values -----------------------------------------------------
def access_obj_values():
    import pyomo.environ as pyo
    from pyomo.opt import SolverFactory
    # Create a solver
    opt = SolverFactory('glpk')
    # A simple model with binary variables and
    # an empty constraint list.
    model = pyo.ConcreteModel()
    model.n = pyo.Param(default=4)
    model.x = pyo.Var(pyo.RangeSet(model.n), within=pyo.Binary)
    # Note: model.x creates an interable using rangeset and returns
    # 4 values of x indexed using the vals created in the rangeset funct.
    [print(model.x[i]) for i in range(1,5)]
    def o_rule(model):
        return summation(model.x)
    model.o = pyo.Objective(rule=o_rule)
    model.c = pyo.ConstraintList()
    results = opt.solve(model)

    # Print All Variables
    for v in model.component_objects(pyo.Var, active=True):
        print("Variable",v)
        # Print All Values Assigned to variables
        for index in v:
            print ("   ",index, pyo.value(v[index]))

    # Print All Parameters
    for parmobject in model.component_objects(pyo.Param, active=True):
        nametoprint = str(str(parmobject.name))
        print ("Parameter ", nametoprint)  # doctest: +SKIP
        for index in parmobject:
            vtoprint = pyo.value(parmobject[index])
            print ("   ",index, vtoprint)  # doctest: +SKIP

access_obj_values()






















