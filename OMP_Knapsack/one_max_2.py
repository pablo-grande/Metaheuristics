#!/usr/bin/env python
# -*- coding: utf-8 -*
import random

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from deap import base, creator, tools, algorithms

ONE_MAX_LENGTH = 100
POPULATION_SIZE = 200
P_CROSSOVER = 0.9
P_MUTATION = 0.1
MAX_GENERATION = 50

RANDOM_SEED = 42

toolbox = base.Toolbox()
toolbox.register("zeroOrOne", random.randint, 0, 1)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox.register(
    "individualCreator",
    tools.initRepeat,
    creator.Individual,
    toolbox.zeroOrOne,
    ONE_MAX_LENGTH,
)
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

def oneMaxFitness(individual):
    return (sum(individual),)


toolbox.register("evaluate", oneMaxFitness)

toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", tools.cxOnePoint)

toolbox.register("mutate", tools.mutFlipBit, indpb=1.0 / ONE_MAX_LENGTH)

def main():
    population = toolbox.populationCreator(n=POPULATION_SIZE)

    stats = tools.Statistics(lambda individual: individual.fitness.values)
    stats.register("max", np.max)
    stats.register("avg", np.mean)

    population, logbook = algorithms.eaSimple(
        population,
        toolbox,
        cxpb=P_CROSSOVER,
        mutpb=P_MUTATION,
        ngen=MAX_GENERATION,
        stats=stats,
        verbose=True,
    )

    max_fitness_values, mean_fitness_values = logbook.select("max", "avg")

    sns.set_style("whitegrid")
    plt.plot(max_fitness_values, color="red")
    plt.plot(mean_fitness_values, color="green")
    plt.xlabel("Generation")
    plt.ylabel("Max/Average Fitness")
    plt.title("Max and Average Fitness over Generations")
    plt.show()


if __name__ == "__main__":
    main()

