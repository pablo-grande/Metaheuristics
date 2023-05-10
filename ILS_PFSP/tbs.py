#!/usr/bin/env python
# -*- coding: utf-8 -*
from datasets import berlin_52 as inputTSP
from math import sqrt
from random import randrange
from time import time

def timeit(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func

def locate_best_new_sol(new_solutions):
    new_solutions.sort(key=lambda c: c["cost"])
    return new_solutions[0]


def is_tabu(permutation, tabu_list):
    size = len(permutation)
    for index, node in enumerate(permutation):
        next_node = [permutation[0] if index == size - 1 else permutation[index+1]]
        edge = [node, next_node]
        if edge in tabu_list:
            return True
    return False


def euclidean_distance(start_node, end_node):
    _sum = 0.0
    for xi, yi in zip(start_node, end_node):
        _sum += pow((xi - yi), 2)
    return sqrt(_sum)



def stochastic_two_opt_with_edges(permuation):
    result = permuation[:]
    size = len(result)
    p1, p2 = randrange(0, size), randrange(0, size)
    exclude = set([p1])
    exclude.add(size - 1 if p1 == 0 else p1 - 1)
    exclude.add(0 if p1 == size - 1 else p1 + 1)
    while p2 in exclude:
        p2 = randrange(0, size)

    if p2 < p1:
        p1, p2 = p2, p1

    result[p1:p2] = reversed(result[p1:p2])
    return result, [[permuation[p1-1], permuation[p1]], [permuation[p2-1], permuation[p2]]]


def generate_new_solution(base_solution, best_solution, tabu_list):
    new_permutation, edges, new_solution = None, None, {}
    while new_permutation == None or is_tabu(new_permutation, tabu_list):
        new_permutation, edges = stochastic_two_opt_with_edges(base_solution["permutation"])
        if tour_cost(new_permutation) < best_solution["cost"]:
            break

    new_solution["permutation"] = new_permutation
    new_solution["cost"] = tour_cost(new_solution["permutation"])
    new_solution["edges"] = edges
    return new_solution




def construct_initial_solution(init_permutation):
    permutation = init_permutation[:]
    size = len(permutation)
    for index in range(size):
        shuffle_index = randrange(index, size)
        permutation[shuffle_index], permutation[index] = permutation[index], permutation[shuffle_index]
    return permutation


def tour_cost(permutation):
    total_distance = 0.0
    size = len(permutation)
    for index in range(size):
        start_node = permutation[index]
        end_node = permutation[0] if index == size - 1 else permutation[index + 1]
        total_distance += euclidean_distance(start_node, end_node)
    return total_distance


@timeit
def tbs(max_new_solutions, max_iterations, max_edges_in_tabu_list=10, k=5):
    best_solution = {
        "edges": None,
        "permutation": construct_initial_solution(inputTSP)
    }
    best_solution["cost"] = tour_cost(best_solution["permutation"])
    base_solution = best_solution

    credit = 0
    tabu_list = []

    while max_iterations > 0:
        new_solutions = []
        for index in range(0, max_new_solutions):
            new_solution = generate_new_solution(base_solution, best_solution, tabu_list)
            new_solutions.append(new_solution)

        best_new_solution = locate_best_new_sol(new_solutions)
        delta = best_new_solution["cost"] - base_solution["cost"]
        if delta <= 0:
            credit = -1 * delta
            base_solution = best_new_solution

            if best_new_solution["cost"] < best_solution["cost"]:
                best_solution = best_new_solution
                print(f"it: {max_iterations} cost: {best_solution['cost']:.2f}")
                for edge in best_new_solution["edges"]:
                    tabu_list.append(edge)
                    if len(tabu_list) > max_edges_in_tabu_list:
                        del tabu_list[0]
        else:
            if delta <= k * credit:
                credit = 0
                base_solution = best_new_solution
        max_iterations -= 1


max_new_solutions = [20, 40, 60]
max_iterations = [1000, 2500, 5000]
for max_new_solution in max_new_solutions:
    for max_iteration in max_iterations:
        tbs(max_new_solution, max_iteration)