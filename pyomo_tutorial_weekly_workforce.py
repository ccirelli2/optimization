# -*- coding: utf-8 -*-
"""
** This example is too hard to follow and or is too complex for understanding
the basics of pyomo. 

Ref : https://protect-us.mimecast.com/s/9ajwC31p1kiv12jugIpP8?domain=link.medium.com
Topic :  modeling and solution finding of a scheduling problem where workers 
have to be assigned to shifts to optimize given criteria, satisfying diverse
imposed constraints to the working conditions.


"""

# Import Libraries ------------------------------------------------------------
from pyomo.environ import *
from pyomo.opt import SolverFactory

# Build Concrete Model --------------------------------------------------------
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
shifts = ['Morning', 'Evening', 'Night']  # 3 shifts of 8 hours
days_shifts = {day: shifts for day in days}
workers = ['W' + str(i) for i in range(1, 11)]

# Initialize Model ------------------------------------------------------------
'''
Basically every possible combination of worker, day, shift
test = [(worker, day, shift) for worker in workers for day in days for shift in days_shifts[day]]
'''
model = ConcreteModel()
model.works = Var(((worker, day, shift) for worker in workers for day in days for shift in days_shifts[day]), within=Binary, initialize=0)

# binary variables representing if a worker is necessary
model.needed = Var(workers, within=Binary, initialize=0)

# binary variables representing if a worker worked on sunday but not on saturday (avoid if possible)
model.no_pref = Var(workers, within=Binary, initialize=0)

# Define An Objective Function ------------------------------------------------
# Define an objective function with model as input, to pass later
def obj_rule(m):
    c = len(workers)
    return sum(m.no_pref[worker] for worker in workers) + sum(c * m.needed[worker] for worker in workers)
# we multiply the second term by a constant to make sure that it is the primary objective
# since sum(m.no_prefer) is at most len(workers), len(workers) + 1 is a valid constant.


# add objective function to the model. rule (pass function) or expr (pass expression directly)
model.obj = Objective(rule=obj_rule, sense=minimize)








