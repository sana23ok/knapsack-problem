# Задача про рюкзак (місткість P=150, 100 предметів, цінність предметів від 2 до
# 10 (випадкова), вага від 1 до 5 (випадкова)), генетичний алгоритм (початкова популяція
# 100 осіб кожна по 1 різному предмету, оператор схрещування рівномірний, мутація з ймовірністю
# 5% два випадкові гени міняються місцями). Розробити власний оператор локального покращення.

#Зафіксувати якість отриманого розв'язку (значення цільової функції) після кожних 20 ітерацій до 1000

from items_generator import ItemsGenerator
from solver import KnapsackSolver

file_name = "items.txt"
carrier_limit = 150
population_size = 100
generation_size = 100
mutation_rate = 0.05
items_count = 100
min_w = 1
max_w = 5
min_c = 2
max_c = 10


def run_algo():
    Data = ItemsGenerator(file_name, min_w, max_w, min_c, max_c, items_count)
    Data.generateItems()
    Knapsack = KnapsackSolver(file_name,
                              carrier_limit,
                              population_size,
                              generation_size,
                              mutation_rate)
    Knapsack.find_solution()


if __name__ == '__main__':
    run_algo()
