#!/usr/bin/env python
# -*- coding: utf-8 -*
import random

import matplotlib.pyplot as plt
import seaborn as sns
import numpy

from deap import base, creator, tools, algorithms

from knapsack import Knapsack


knapsack = Knapsack()

population_size = 50
crossover = 0.9
mutation = 0.1
max_generations = 50
hall_of_fame_size = 1

seed = 42
random.seed(seed)

toolbox = base.Toolbox()
toolbox.register("zero_or_one", random.randint, 0, 1)
creator.create("fitness_max", base.Fitness, weights=(1.0,))
creator.create("individual", list, fitness=creator.fitness_max)
toolbox.register(
    "individual_creator",
    tools.initRepeat,
    creator.individual,
    toolbox.zero_or_one,
    len(knapsack),
)
toolbox.register(
    "population_creator", tools.initRepeat, list, toolbox.individual_creator
)


def knapsack_value(individual):
    return (knapsack.get_value(individual),)


toolbox.register("evaluate", knapsack_value)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=1.0 / len(knapsack))


def main():
    population = toolbox.population_creator(n=population_size)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("max", numpy.max)
    stats.register("avg", numpy.mean)

    hof = tools.HallOfFame(hall_of_fame_size)

    population, logbook = algorithms.eaSimple(
        population,
        toolbox,
        cxpb=crossover,
        mutpb=mutation,
        ngen=max_generations,
        stats=stats,
        halloffame=hof,
        verbose=True,
    )
    best = hof.items[0]
    print(f"-- Best Ever Individual = {best}")
    print(f"-- Best Ever Fitness = {best.fitness.values[0]}")
    print(f"-- Knapsack Items = {knapsack.print_items(best)}")

    max_fitness_values, mean_fitness_values = logbook.select("max", "avg")

    sns.set_style("whitegrid")
    plt.plot(max_fitness_values, color="red")
    plt.plot(mean_fitness_values, color="blue")
    plt.xlabel("Generation")
    plt.ylabel("Max/Avg. Fitness")
    plt.title("Max and Average fitness over generations")
    plt.show()


if __name__ == "__main__":
    main()
