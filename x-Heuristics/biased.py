from math import log
from random import random


efficiency_list = [2, 1, 3, 4, 6, 5, 7, 9, 0, 8]
efficiency_list.sort(reverse=True)

alpha = 0.9

for i in range(10):
    eff_list = efficiency_list.copy()
    store_list = []
    for _ in range(len(eff_list)):
        index = int(log(random())/log(1-alpha))
        index = index % len(eff_list)
        store_list.append(eff_list[index])
        eff_list.pop(index)

    print(i, store_list)