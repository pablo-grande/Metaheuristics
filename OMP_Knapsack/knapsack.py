#!/usr/bin/env python
# -*- coding: utf-8 -*
import numpy as np


class Knapsack:
    def __init__(self, max_capacity=400):
        self.max_capacity = max_capacity
        self.items = [
            ("map", 9, 150),
            ("compass", 13, 35),
            ("sandwich", 153, 200),
            ("glucose", 50, 160),
            ("tin", 15, 60),
            ("banana", 68, 45),
            ("apple", 39, 40),
            ("cheese", 23, 30),
            ("beer", 52, 10),
            ("suntan", 11, 70),
            ("camera", 32, 30),
            ("t-shirt", 24, 15),
            ("trousers", 48, 10),
            ("umbrella", 73, 40),
            ("waterproof clothes", 42, 75),
            ("sunglasses", 7, 20),
            ("socks", 18, 12),
            ("towel", 4, 50),
            ("book", 30, 10),
        ]

    def __len__(self):
        return len(self.items)

    def get_value(self, zero_one_list):
        total_weight = total_value = 0
        for i in range(len(zero_one_list)):
            item, weight, value = self.items[i]
            if total_weight + weight <= self.max_capacity:
                total_weight += zero_one_list[i] * weight
                total_value += zero_one_list[i] * value
        return total_value

    def print_items(self, zero_one_list):
        total_weight = total_value = 0
        for i in range(len(zero_one_list)):
            item, weight, value = self.items[i]
            if zero_one_list[i] > 0:
                total_weight += weight
                total_value += value
                print(f"- Adding {item}: weight = {weight}, value = {value}, accumulated weight = {total_weight}, accumulated value = {total_value}")
        print(f"- Total weight = {total_weight}, Total value = {total_value}")

def main():
    knapsack = Knapsack()
    random_solution = np.random.randint(2, size=len(knapsack))
    print(f"Random solution = {random_solution}")
    knapsack.print_items(random_solution)

if __name__ == "__main__":
    main()
