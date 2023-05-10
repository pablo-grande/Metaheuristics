#!/usr/bin/env python
# -*- coding: utf-8 -*
import random

import matplotlib.pyplot as plt
import seaborn as sns

from deap import base, creator, tools

ONE_MAX_LENGTH = 100
POPULATION_SIZE = 200
P_CROSSOVER = 0.9
P_MUTATION = 0.1
MAX_GENERATION = 50

RANDOM_SEED = 42

random.seed(RANDOM_SEED)

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
    generation_counter = 0

    fitness_values = list(map(toolbox.evaluate, population))
    for individual, fitness_values in zip(population, fitness_values):
        individual.fitness.values = fitness_values

    fitness_values = [individual.fitness.values[0] for individual in population]

    max_fitness_values, mean_fitness_values = [], []
    while max(fitness_values) < ONE_MAX_LENGTH and generation_counter < MAX_GENERATION:
        generation_counter += 1
        offspring = toolbox.select(population, len(population))
        for c1, c2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < P_CROSSOVER:
                toolbox.mate(c1, c2)
                del c1.fitness.values
                del c2.fitness.values

        for individual in offspring:
            if random.random() < P_MUTATION:
                toolbox.mutate(individual)
                del individual.fitness.values

        fresh_individuals = [
            individual for individual in offspring if not individual.fitness.valid
        ]
        fresh_fitness_values = list(map(toolbox.evaluate, fresh_individuals))
        for individual, fitness_value in zip(fresh_individuals, fresh_fitness_values):
            individual.fitness.values = fitness_value

        population[:] = offspring
        fitness_values = [individual.fitness.values[0] for individual in population]

        max_fitness = max(fitness_values)
        mean_fitness = sum(fitness_values) / len(population)
        max_fitness_values.append(max_fitness)
        mean_fitness_values.append(mean_fitness)
        print(
            f"- Generation {generation_counter}: Max Fitness = {max_fitness}, Avg. Fitness = {mean_fitness}"
        )
        best_index = fitness_values.index(max(fitness_values))
        print("Best Individual = ", *population[best_index])

    sns.set_style("whitegrid")
    plt.plot(max_fitness_values, color="red")
    plt.plot(mean_fitness_values, color="green")
    plt.xlabel("Generation")
    plt.ylabel("Max/Average Fitness")
    plt.title("Max and Average Fitness over Generations")
    plt.show()


if __name__ == "__main__":
    main()
