# -*- coding: utf-8 -*-
"""
Ref : https://nbviewer.jupyter.org/github/Pyomo/PyomoGallery/blob/master/diet/DietProblem.ipynb

Summary :
The goal of the Diet Problem is to select foods that satisfy daily nutritional requirements at minimum cost. This problem can be formulated as a linear
program, for which constraints limit the number of calories and the amount of
vitamins, minerals, fats, sodium, and cholesterol in the diet. Danzig (1990)
notes that the diet problem was motivated by the US Army's desire to minimize
the cost of feeding GIs in the field while still providing a healthy diet.
"""

# Import Pyomo Package
from pyomo.environ import *
infinity = float('inf')

# Create a Model Object
model = AbstractModel()

# Create Sets For Food & Nutrients
model.F = Set()
model.N = Set()

# Define Model Parameters Abstractly

# Cost of Each Food
model.c = Param(model.F, within=PositiveReals)
# Amount of Nutrients in Each Food
'Note that by passing in Model F and N we are creating an FxN matrix'
model.a = Param(model.F, model.N, within=NonNegativeReals)


# Create Lower & Upper Bounds Of Each Nutrient
model.Nmin = Param(model.N, within=NonNegativeReals, default=0.0)
model.Nmax = Param(model.N, within=NonNegativeReals, default=infinity)

# Volume per serving of food
model.V    = Param(model.F, within=PositiveReals)

# Maximum volume of food consumed
model.Vmax = Param(within=PositiveReals)

# Number of servings consumed of each food
model.x = Var(model.F, within=NonNegativeIntegers)


## Define Objective Function --------------------------------------------------

# Minimize the cost of food that is consumed
'sum of cost * servings for each value in the set of model.F'
def cost_rule(model):
    return sum(model.c[i]*model.x[i] for i in model.F)
model.cost = Objective(rule=cost_rule, sense=minimize)

## Define Constraints ---------------------------------------------------------

# Limit nutrient consumption for each nutrient
def nutrient_rule(model, j):
    value = sum(model.a[i,j]*model.x[i] for i in model.F)
    return model.Nmin[j] <= value <= model.Nmax[j]
model.nutrient_limit = Constraint(model.N, rule=nutrient_rule)


# Limit the volume of food consumed
def volume_rule(model):
    return sum(model.V[i]*model.x[i] for i in model.F) <= model.Vmax
model.volume = Constraint(rule=volume_rule)






