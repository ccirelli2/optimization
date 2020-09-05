# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 10:37:16 2020

@author: chris.cirelli
"""
# Import Libraries ------------------------------------------------------------
from pyomo.environ import *
import numpy as np

def ex_indexed_constraint():
    model = ConcreteModel()
    model.A = Set(initialize=[1,2,3])
    model.A.display()
    def d_rule(model, a):
        return a*model.x <=0
    model.d = Constraint(model.A, rule=d_rule)


def create_var_pass_dict():
    test = [1, 2, 3, 4]
    model = ConcreteModel()
    # Create Set Object Index & Initial Values Using List
    model.b = Var(initialize={'A':1, 'B':2, 'C':3, 'D':4})
    model.b.display()


def create_var_set_vals():
    model = ConcreteModel()
    test = [0,2,4,6]
    model.a = Set(initialize=[1,2,3,4])
    model.a.display()
    def assig_vals(m, i):
        return i + 0.5
    model.b = Var(model.a, initialize=assig_vals)
    model.b.display()
    model.c = Var(bounds=(1, 2))
    print('Model Upper Bound => {}'.format(model.c.ub))
    print('Model Lower Bound => {}'.format(model.c.lb))


def create_var_fixed_vals():
    model = ConcreteModel()
    indx = [1,2,3]
    model.A = Set(initialize=[1,2,3])
    model.ab = Var(model.A, initialize={1:1.5, 2:4.5, 3:5.5})

    # Fix values of model.ab
    for i in indx:
        model.ab[i].fix(i)
    model.ab.display()



def create_var_fixed_vals_v2():
    model = ConcreteModel()
    premiums = np.random.randint(1, 100, 10)
    incurred = np.random.randint(1, 7, 10)
    indx = [x for x in range(0, 10)]
    # Build Dictionary
    dict_prems = {}
    for x,y in zip(indx, premiums):
        dict_prems[x] = y
    model.A = Var(indx, initialize=dict_prems)
    model.A.display()
    # Fix Model.A Values
    [model.A[key].fix(model.A[key].value) for key in dict_prems]
    model.A.display()
    # Create Sum of Premium Value From Model.A
    sum_prem = sum([model.A[key].value for key in dict_prems])
    model.B = Var(initialize=sum_prem)
    model.B.fix(sum_prem)
    model.B.display()

create_var_fixed_vals_v2()







