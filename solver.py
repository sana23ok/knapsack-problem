import random
from matplotlib import pyplot as plt
import items


class KnapsackSolver:
    def __init__(self, file_name: str, carrier_limit: int, population_size: int,
                 generation_size: int, mutation_rate: float):
        self.__file = file_name
        self.__carrier_limit = carrier_limit
        self.__population_size = population_size
        self.__generation_size = generation_size
        self.__mutation_rate = mutation_rate
        self.__items_list = []  # list of objects of class Item
        self.__value_list = []

    def read_input(self):
        with open(self.__file, "r") as f:
            for line in f:
                new_line = line.strip()
                new_line = new_line.split(" ")
                id, w, v = new_line[0], new_line[1], new_line[2]
                # check dataset file to see why id,w,v = 0,1,2
                new_item = items.Item(int(id), float(w), float(v))
                self.__items_list.append(new_item)

    def create_random_solution(self, i_list):
        solution = []
        for i in range(0, len(i_list)):
            solution.append(random.randint(0, 1))
        return solution

    def valid_solution(self, i_list, s_list, limit):
        total_weight = 0
        for i in range(0, len(s_list)):
            if s_list[i] == 1:
                total_weight += i_list[i].weight
            if total_weight > limit:
                return False
        return True

    def calculate_value(self, i_list, s_list):
        total_value = 0
        for i in range(0, len(s_list)):
            if s_list[i] == 1:
                total_value += i_list[i].value
        return total_value

    def check_duplicate_solutions(self, S1, S2):
        for i in range(0, len(S1)):
            if S1[i] != S2[i]:
                return False
        return True

    def initial_population(self, pop_size, i_list, w_limit):
        population = []
        i = 0
        while i < pop_size:
            new_solution = self.create_random_solution(i_list)
            if self.valid_solution(i_list, new_solution, w_limit):
                if len(population) == 0:
                    population.append(new_solution)
                    i += 1
                else:
                    skip = False
                    for j in range(0, len(population)):
                        if self.check_duplicate_solutions(new_solution, population[j]):
                            skip = True
                            continue
                    if not skip:
                        population.append(new_solution)
                        i += 1
        return population

    def tournament_selection(self, pop):
        ticket_1 = random.randint(0, len(pop) - 1)
        ticket_2 = random.randint(0, len(pop) - 1)
        if self.calculate_value(self.__items_list, pop[ticket_1]) > \
                self.calculate_value(self.__items_list, pop[ticket_2]):
            winner = pop[ticket_1]
        else:
            winner = pop[ticket_2]
        return winner

    def crossover(self, p1, p2):
        break_point = random.randint(0, len(p1))
        first_part = p1[:break_point]
        second_part = p2[break_point:]
        child = first_part + second_part
        if self.valid_solution(self.__items_list, child, self.__carrier_limit):
            return child
        else:
            return self.crossover(p1, p2)

    def mutation(self, chromosome):
        temp = chromosome.copy()  # Create a copy of the chromosome
        mutation_index_1, mutation_index_2 = random.sample(range(0, len(chromosome)), 2)
        temp[mutation_index_1], temp[mutation_index_2] = temp[mutation_index_2], temp[mutation_index_1]

        if self.valid_solution(self.__items_list, temp, self.__carrier_limit):
            return temp
        else:
            return self.mutation(chromosome)

    def create_generation(self, pop, mut_rate):
        new_gen = []
        for i in range(0, len(pop)):
            parent_1 = self.tournament_selection(pop)
            parent_2 = self.tournament_selection(pop)
            child = self.crossover(parent_1, parent_2)
            if random.random() < mut_rate:
                child = self.mutation(child)
            new_gen.append(child)
        return new_gen

    def best_solution(self, generation, i_list):
        best = 0
        for i in range(0, len(generation)):
            temp = self.calculate_value(i_list, generation[i])
            if temp > best:
                best = temp
        return best

    def genetic_algorithm(self, c_limit, p_size, gen_size, mutation_rate, i_list):
        pop = self.initial_population(p_size, i_list, c_limit)
        for i in range(0, gen_size):
            pop = self.create_generation(pop, mutation_rate)
            print(pop[0])

            print("value => ", self.calculate_value(i_list, pop[0]))
            self.__value_list.append(self.best_solution(pop, i_list))
        return pop, self.__value_list

    def find_solution(self):
        self.read_input()
        latest_pop, v_list = self.genetic_algorithm(self.__carrier_limit,
                                                    self.__population_size,
                                                    self.__generation_size,
                                                    self.__mutation_rate,
                                                    self.__items_list)

        plt.plot(v_list)
        plt.xlabel('generations')
        plt.ylabel('values')
        plt.title("Values of the solutions during the generations")
        plt.show()
