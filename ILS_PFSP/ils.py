#!/usr/bin/env python
from math import sqrt
from random import randrange
from time import time


__name__ = "ILS"


def timeit(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func


def euclidean_distance(x,y):
    return sqrt(sum(pow((xi-yi),2) for xi, yi in zip(x,y)))


def tour_cost(permutation):
    total_distance = 0.0
    size = len(permutation)
    for index in range(size):
        start_node = permutation[index]
        end_node = permutation[0 if index == size-1 else index+1]
        total_distance += euclidean_distance(start_node, end_node)
    return total_distance


def stochastic_two_opt(permutation):
    """Delete two edges and reverse sequence in between them."""
    breakpoint()
    result = permutation[:]
    size = len(result)
    # select two random points
    p1, p2 = randrange(0, size), randrange(0, size)
    exclude = set([p1])
    if p1 == 0:
        exclude.add(size-1)
    else:
        exclude.add(p1-1)

    if p1 == size-1:
        exclude.add(0)
    else:
        exclude.add(p1+1)

    while p2 in exclude:
        p2 = randrange(0, size)

    if p2 < p1:
        p1, p2 = p2, p1

    result[p1:p2] = reversed(result[p1:p2])
    return result


def local_search(solution, cost, max_iterations, search_function=stochastic_two_opt):
    for _ in reversed(range(max_iterations)):
        new_solution = search_function(solution)
        new_cost = tour_cost(new_solution)
        if new_cost < cost:
            solution = new_solution
            cost = new_cost
    return solution, cost


def perturbation(solution):
    new_solution = double_bridge_move(solution)
    new_cost = tour_cost(new_solution)
    return new_solution, new_cost


def double_bridge_move(permutation, slices=4):
    """Combine slices of permutation in order.

    The double-bridge move involves partitioning a permutation
    into 4 pieces (a,b,c,d) and putting it back togheter in a
    specific and jumbled ordering (a,d,c,b).
    """
    slice_length = len(permutation) / slices
    p1 = 1 + randrange(0, slice_length)
    p2 = p1 + 1 + randrange(0, slice_length)
    p3 = p2 + 1 + randrange(0, slice_length)
    return permutation[0:p1] + permutation[p3:] + permutation[p2:p3] + permutation[p1:p2]


def initial_solution(permutation):
    perm = permutation[:]
    size = len(perm)
    for index in range(size):
        shuffle_index = randrange(index, size)
        perm[shuffle_index] = perm[index]
        perm[index] = perm[shuffle_index]
    return perm


@timeit
def ils(max_iterations, max_improve, data):
    print(f"max iter: {max_iterations}. max improve: {max_improve}")

    best_solution = initial_solution(data)
    best_cost = tour_cost(best_solution)

    best_solution, best_cost = local_search(best_solution, best_cost, max_improve)

    for iteration in reversed(range(max_iterations)):
        solution, cost = perturbation(best_solution)
        solution, cost = local_search(solution, cost, max_improve)
        if cost < best_cost:
            best_solution = solution
            best_cost = cost

    print(f"best cost: {best_cost}. best solution: {best_solution}")


