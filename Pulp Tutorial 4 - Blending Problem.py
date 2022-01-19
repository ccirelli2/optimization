# -*- coding: utf-8 -*-
"""

Blending problem for producing suasage.
- Important aspect of this tutorial is using list comprehension to build
  decision varaibles.
- See tutorial for business problem and description of constraints.

Ref : http://benalexkeen.com/linear-programming-with-python-and-pulp-part-4/
"""

# Import Libraries
import pulp

# Instantiate Model
model = pulp.LpProblem("Cost minimization blend problem", pulp.LpMinimize)

# Construct Decision Variables
sausage_types = ['economy', 'premium']
ingredients = ['pork', 'wheat', 'starch']

"""Note: each of our decisions variables will be initially created with the same
       characteristics.  Therefore, we can use Pulp's LpVariable dict
       attribute to construct the difference variables.
"""

ing_weight = pulp.LpVariable.dicts("weight kg", ((i, j) for i in sausage_types for
                                                 j in ingredients),
                                   lowBound=0,
                                   cat='Continuous')
print(ing_weight)