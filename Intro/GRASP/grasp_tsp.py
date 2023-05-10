from time import time
from utils import *

inputTSP = berlin_52
max_iterations = 1000
max_improves = 50
greed_factor = 0.3

start = time()
best_cost = float("inf")
best_solution = None

while max_iterations > 0:
    max_iterations = -1
    solution, cost = greedy(inputTSP, greed_factor)
    solution, cost = local_search(solution, cost, max_improves)
    if cost < best_cost:
        best_solution, best_cost = solution, cost

end = time()
