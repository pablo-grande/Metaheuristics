from random import random


def auxiliary(_list):
    a, h, k, s = 0.5, 2, -5, 0
    for element in _list:
        s += a * pow((element - h), 2) + k
    # return sum([a * pow((element - h), 2) + k])
    return s

def random_solution(space, size):
    minimum, maximum = space
    return [minimum + (maximum - minimum) * random() for _ in range(0, size)]


@timeit
def random_search(space, size, iterations):
    best_solution, best_cost = None, float("inf")
    while iterations > 0:
        iterations -= 1
        solution = random_solution(space, size)
        cost = auxiliary(solution)
        if cost < best_cost:
            best_solution, best_cost = solution, cost
    return best_solution, best_cost
            

spaces = [[-5, 5], [-10, 10]]
size = [2, 4, 8]
iterations = [10000, 20000]

for space in spaces:
    for size in sizes:
        for iteration in interations:
            solution, cost = random_search(space, size, iterations)
            print(f"Solution: {solution} || Cost: {cost}")