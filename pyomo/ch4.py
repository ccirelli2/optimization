# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 10:37:16 2020

@author: chris.cirelli
"""
# Import Libraries ------------------------------------------------------------
from pyomo.environ import *

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
    vals = [x.values() for x in model.ab]
    print('Var => model.ab, Varlues => {}'.format(vals))










