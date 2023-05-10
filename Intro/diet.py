from pyomo.environ import *


model = AbstractModel()

model.FOOD = Set()
model.cost = Param(model.FOOD, within=PositiveReals)

model.f_min = Param(model.FOOD, within=NonNegativeReals, default=0.0)

def f_max_validate (model, food):
    return model.f_max[food] > model.f_min[food]
model.f_max = Param(model.FOOD, validate=f_max_validate, default=20.0)

model.NUTR = Set()
model.n_min = Param(model.NUTR, within=NonNegativeReals, default=0.0)
model.n_max = Param(model.NUTR, default=float("inf"))
model.amt = Param(model.NUTR, model.FOOD, within=NonNegativeReals)

model.servings = Var(model.FOOD, within=NonNegativeIntegers)

def total_cost_rule(model):
    return sum(model.cost[food] * model.servings[food] for food in model.FOOD)
model.total_cost = Objective(rule=total_cost_rule, sense=minimize)


def nutrient_rule(model, nutrient):
    limit = sum(model.amt[nutrient, food] * model.servings[food] for food in model.FOOD)
    return (model.n_min[nutrient], limit, model.n_max[nutrient])
model.nutrient_limit = Constraint(model.NUTR, rule=nutrient_rule)
