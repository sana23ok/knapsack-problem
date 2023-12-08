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

    def __read_input(self):
        with open(self.__file, "r") as f:
            for line in f:
                new_line = line.strip()
                new_line = new_line.split(" ")
                id, w, v = new_line[0], new_line[1], new_line[2]
                # check dataset file to see why id,w,v = 0,1,2
                new_item = items.Item(int(id), float(w), float(v))
                self.__items_list.append(new_item)

    @staticmethod
    def __create_random_solution(i_list):
        solution = []
        for i in range(0, len(i_list)):
            solution.append(random.randint(0, 1))
        return solution

    def __valid_solution(self, i_list, s_list):
        total_weight = 0
        for i in range(0, len(s_list)):
            if s_list[i] == 1:
                total_weight += i_list[i].weight
            if total_weight > self.__carrier_limit:
                return False
        return True

    @staticmethod
    def __totalValue(i_list, s_list):
        total_value = 0
        for i in range(0, len(s_list)):
            if s_list[i] == 1:
                total_value += i_list[i].value
        return total_value

    @staticmethod
    def __totalWeight(i_list, s_list):
        total_weight = 0
        for i in range(0, len(s_list)):
            if s_list[i] == 1:
                total_weight += i_list[i].weight
        return total_weight

    @staticmethod
    def __check_duplicate_solutions(S1, S2):
        for i in range(0, len(S1)):
            if S1[i] != S2[i]:
                return False
        return True

    def __initial_population(self, pop_size, i_list):
        population = []
        i = 0
        while i < pop_size:
            new_solution = self.__create_random_solution(i_list)
            if self.__valid_solution(i_list, new_solution):
                if len(population) == 0:
                    population.append(new_solution)
                    i += 1
                else:
                    skip = False
                    for j in range(0, len(population)):
                        if self.__check_duplicate_solutions(new_solution, population[j]):
                            skip = True
                            continue
                    if not skip:
                        population.append(new_solution)
                        i += 1
        return population

    #Турнірна селекція: з популяції Р випадковим чином вибирається деяка
    # підмножина і батьком призначається найкраще рішення в P множині
    def __tournament_selection(self, curr_population):
        variant_1 = random.randint(0, len(curr_population) - 1)
        variant_2 = random.randint(0, len(curr_population) - 1)
        # обрахування придатності вибраних особин
        if self.__totalValue(self.__items_list, curr_population[variant_1]) > \
                self.__totalValue(self.__items_list, curr_population[variant_2]):
            winner = curr_population[variant_1]
        else:
            winner = curr_population[variant_2]
        return winner

    # рівномірний кросиновер, кожен ген від батьків передається випадковим чином з ймовірністю 0,5.
    def __equal_crossover(self, p1, p2):
        child = []  # list with the genes of the child
        for gene1, gene2 in zip(p1, p2):
            prob = random.randint(0, 1)
            if prob < 0.5:
                child.append(gene1)
            else:
                child.append(gene2)

        if self.__valid_solution(self.__items_list, child):
            return child
        else:
            return self.__equal_crossover(p1, p2)

    @staticmethod
    def __swap(lst, index1, index2):
        lst[index1], lst[index2] = lst[index2], lst[index1]

    def __mutation(self, chromosome):
        temp = chromosome.copy() # копія хромосоми
        mutation_index_1, mutation_index_2 = random.sample(range(0, len(chromosome)), 2)
        # обрано два випадкових індекси в хромосомі
        self.__swap(temp, mutation_index_1, mutation_index_2)
        if self.__valid_solution(self.__items_list, temp):
            return temp
        else:
            return self.__mutation(chromosome)

    def __create_generation(self, pop, mut_rate):
        new_gen = []
        for i in range(0, len(pop)):
            S1 = self.__tournament_selection(pop)
            S2 = self.__tournament_selection(pop)
            child = self.__equal_crossover(S1, S2)
            if random.random() < mut_rate:
                child = self.__mutation(child)
            new_gen.append(child)
        return new_gen

    def __goal_solution(self, generation, i_list):
        best = 0
        for i in range(0, len(generation)):
            temp = self.__totalValue(i_list, generation[i])
            if temp > best:
                best = temp
        return best

    def genetic_algorithm(self, p_size, gen_size, mutation_rate, i_list):
        pop = self.__initial_population(p_size, i_list)
        counter = 0
        for i in range(0, gen_size):
            pop = self.__create_generation(pop, mutation_rate)

            # Print information for iterations divisible by 20
            if counter % 20 == 0:
                print(f"Iteration {counter}")
                print("Best solution:", pop[0])
                print("Value:", self.__totalValue(i_list, pop[0]))
                print("Weight:", self.__totalWeight(i_list, pop[0]))

            self.__value_list.append(self.__goal_solution(pop, i_list))
            counter += 1
        print(f"Total count of iterations: {counter}")
        return pop, self.__value_list

    def find_solution(self):
        self.__read_input()
        iter_limit = 1000
        latest_pop, v_list = self.genetic_algorithm(self.__population_size,
                                                    iter_limit,
                                                    self.__mutation_rate,
                                                    self.__items_list)

        plt.plot(v_list)
        plt.xlabel('generations')
        plt.ylabel('values')
        plt.title("Values of the solutions during the generations")
        plt.show()
