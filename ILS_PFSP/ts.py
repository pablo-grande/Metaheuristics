from datasets import berlin_52 as input_tsp
from tbs import tbs


max_new_solutions = [20, 40, 60]
max_iterations = [1000, 2500, 5000]
for max_new_solution in max_new_solutions:
    for max_iteration in max_iterations:
        tbs(max_new_solution, max_iteration, input_tsp)
