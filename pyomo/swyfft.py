# -*- coding: utf-8 -*-
"""
"""

# Libraries -------------------------------------------------------------------
from pyomo.environ import*
import os
import numpy as np
import pandas as pd
from datetime import datetime
import logging

# Define Directories ----------------------------------------------------------
dir_coreprof_eda = r'C:\Users\chris.cirelli\Desktop\repositories\CoreProfitability_eda\scripts\Python'
dir_data = r'C:\Users\chris.cirelli\Desktop\repositories\CoreProfitability_eda\output\ordinal_vars\optimization'

# Project Modules -------------------------------------------------------------
os.chdir(dir_coreprof_eda)
import functions_get_loss_ratio_deciles_indv_feature_sampling_w_replacement as m1

# Import Data
os.chdir(dir_data)
data = pd.read_excel('test_data.xlsx')


# Rate Neutral Constraint
'''
P : equals a list or array of premiums
R : Existing rate making factors
x : is our objective variable.  This will be the new rmf that is chosen
    based on minimizing our histogram distance function.
y : the variable we create / instantiate for our premiums, which
    is indexed by P and constrained to non negative reals
s : sum of all premiums
r : rate making factors to be created by model indexed by the existing rate
    making factors
xr : 2d array to capture both the premium and rate
eq_con : A constraint that says that the new premiums that are generated
    cannot be greater than the original premium "rate neutrality"
'''

def test():
    P = [premiums]
    R = [rate_making_factors]
    S = sum(P)
    model.x = Var(P, within=NonNegativeReals)
    model.y = Var(R, within=NonNegativeReals)
    model.xr = Param(model.x, model.y)
    # Rate Equality Constraint
    model.eq_con = Constraint(expr = sum(model.y[p] for p in P) == model.s)
    
    # RMF Cap Constraint
    ''' Iterate over r,x arrays at the same time, multiply them together and 
        set a constraint that none of these products of these two values can be
        greater than 1.25 x'''
    def rmf_increase_rule(model, r, x):
        return sum((model.xr[r]*model.xr[x])/model.xr[x] for r,x in zip(R,P)) <= 1.25    
    model.rmf_con = Constraint(P,R, rule=rmf_increase_rule)



def create_rmf_var_v2(display, debug):
    # Instantiate Model
    model = ConcreteModel()
    # Select Sovler
    solver = SolverFactory('glpk')
    # Declare Variables
    I = RangeSet(0, 3) # returns [0, 1, 2, 3]
    V = RangeSet(4)
    rmf = [0.9, 1.2, 1.0, 1.20]
    prem = [1000, 1000, 1000, 1000]
    model.x = Var(I, within=NonNegativeReals, bounds=(-0.5, 0.5))
    model.limits = ConstraintList()
    # Declare Objective Function
    model.Obj = Objective(expr = sum(((model.x[i]+1) * prem[i])  for i in I),
                          sense=maximize)
    # Add Constraints To Each Value
    # 1.25 - rmf[i] will give us the margin over which we can increase /decrease
    for i in I:
        model.limits.add(model.x[i] <= (1.25 - rmf[i]))
    # Solve
    if debug is False:
        result = solver.solve(model)
        result.write()
        model.solutions.store_to(result)
        print(result.solution)










