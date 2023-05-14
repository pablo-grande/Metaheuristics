from random import randrange
from math import sqrt


def distance(node_1, node_2):
    return sqrt((node_1[0] - node_2[0]) ** 2.0 + (node_1[1] - node_2[1]) ** 2)


def tour_cost(solution):
    total = 0.0
    for i, node in enumerate(solution):
        end_node = solution[0] if i == len(solution) - 1 else solution[i + 1]
        total += distance(node, end_node)
    return total


def stochastic_two_opt(solution):
    permutation = solution[:]
    size = len(permutation)
    c1, c2 = randrange(0, size), randrange(0, size)
    exclude = {c1}
    exclude.add(size - 1 if c1 == 0 else c1 - 1)
    exclude.add(0 if c1 == size - 1 else c1 + 1)

    while c2 in exclude:
        c2 = randrange(0, size)

    if c2 < c1:
        c1, c2 = c2, c1
    permutation[c1:c2] = reversed(permutation[c1:c2])
    return permutation


def local_search(solution, cost, max_iterations):
    counter = 0
    while counter < max_iterations:
        new_solution = stochastic_two_opt(solution)
        new_cost = tour_cost(new_solution)
        if new_cost < cost:
            solution, cost = new_solution, new_cost
        else:
            counter += 1
    return solution, cost


def greedy(solution, greed_factor):
    size = len(solution)
    candidate = [solution[randrange(0, size)]]
    while len(candidate) < size:
        candidates = [node for node in solution if node not in candidate]
        costs = [distance(candidate[len(candidate) - 1], node) for node in candidates]
        min_cost, max_cost = min(costs), max(costs)
        rcl = [
            candidates[i]
            for i, cost in enumerate(costs)
            if cost <= min_cost + greed_factor * (max_cost - min_cost)
        ]
        candidate.append(rcl[randrange(0, len(rcl))])
    return candidate, tour_cost(candidate)


berlin_52 = [
    [565, 575],
    [25, 185],
    [345, 750],
    [945, 685],
    [845, 655],
    [880, 660],
    [25, 230],
    [525, 1000],
    [580, 1175],
    [650, 1130],
    [1605, 620],
    [1220, 580],
    [1465, 200],
    [1530, 5],
    [845, 680],
    [725, 370],
    [145, 665],
    [415, 635],
    [510, 875],
    [560, 365],
    [300, 465],
    [520, 585],
    [480, 415],
    [835, 625],
    [975, 580],
    [1215, 245],
    [1320, 315],
    [1250, 400],
    [660, 180],
    [410, 250],
    [420, 555],
    [575, 665],
    [1150, 1160],
    [700, 580],
    [685, 595],
    [685, 610],
    [770, 610],
    [795, 645],
    [720, 635],
    [760, 650],
    [475, 960],
    [95, 260],
    [875, 920],
    [700, 500],
    [555, 815],
    [830, 485],
    [1170, 65],
    [830, 610],
    [605, 625],
    [595, 360],
    [1340, 725],
    [1740, 245],
]
