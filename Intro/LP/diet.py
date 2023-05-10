from pyomo.environ import *


model = AbstractModel()

model.foods = {}
model.nutrients = {}
model.cost = Param(model.foods, within=PositiveReals)
model.amount = Param(model.foods, model.nutrients, within=NonNegativeReals)

# lower and upper bound on each nutrient
model.min_nutrient = Param(model.nutrients, within=NonNegativeReals, default=0.0)
model.max_nutrient = Param(model.nutrients, within=NonNegativeReals, default=float("inf"))

model.servings = Var(model.foods, within=NonNegativeReals)

def cost_rule(model):
    return sum(model.cost[food] * model.servings[food] for food in model.foods)

def nutrient_rule(model, nutrient):
    limit = sum(model.amount[food, nutrient] * model.servings[food] for food in model.foods)
    return model.min_nutrient[nutrient] <= limit <= model.max_nutrient[nutrient]

# minimize cost of each food
model.cost = Objective(rule=cost_rule)
# limit nutrient consumption of each nutrient
model.nutrient_limit = Constraint(model.nutrients, rule=nutrient_rule)
