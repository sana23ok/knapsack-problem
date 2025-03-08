import random
from matplotlib import pyplot as plt
import items


class KnapsackSolver:
    def __init__(self, file_name: str, carrier_limit: int, population_size: int,
                 generation_size: int, mutation_rate: float, iters: int):
        self.file = file_name
        self.carrier_limit = carrier_limit
        self.population_size = population_size
        self.generation_size = generation_size
        self.mutation_rate = mutation_rate
        self.iterations_limit = iters
        self.items_list = []  # list of objects of class Item
        self.value_list = []

    def read_input(self):
        with open(self.file, "r") as f:
            for line in f:
                new_line = line.strip()
                new_line = new_line.split(" ")
                id, w, v = new_line[0], new_line[1], new_line[2]
                # check dataset file to see why id,w,v = 0,1,2
                new_item = items.Item(int(id), float(w), float(v))
                self.items_list.append(new_item)

    def genetic_algorithm(self, p_size, mutation_rate):
        pop = self._initial_population(p_size)
        counter = 0
        for i in range(0, self.iterations_limit):
            pop = self._create_generation(pop, mutation_rate)

            # print information for iterations divisible by 20
            if counter % 20 == 0:
                print(f"Iteration {counter}")
                # print("Best solution:", pop[0])
                print("Value:", self._totalCost(pop[0]))  # equal to the cost of goal function
                print("Weight:", self._totalWeight(pop[0]))

            self.value_list.append(self._goal_solution(pop))
            counter += 1
        print(f"Total count of iterations: {counter}")
        return pop, self.value_list

    @staticmethod
    def plot_solution_values(values):
        plt.plot(values)
        plt.xlabel('Generations')
        plt.ylabel('Values')
        plt.title("Values of the solutions during the generations")
        plt.show()

    def find_solution(self):
        self.read_input()
        last_population, cost = self.genetic_algorithm(self.population_size, self.mutation_rate)
        self.plot_solution_values(cost)

    def _create_rand_solution(self):
        solution = []
        for _ in range(0, len(self.items_list)):
            solution.append(random.randint(0, 1))
        return solution

    def _is_valid(self, s_list):
        total_weight = 0
        for i in range(0, len(s_list)):
            if s_list[i] == 1:
                total_weight += self.items_list[i].weight
            if total_weight > self.carrier_limit:
                return False
        return True

    def _totalCost(self, s_list):
        total_cost = 0
        for i in range(0, len(s_list)):
            if s_list[i] == 1:
                total_cost += self.items_list[i].value
        return total_cost

    def _totalWeight(self, s_list):
        total_weight = 0
        for i in range(0, len(self.items_list)):
            if s_list[i] == 1:
                total_weight += self.items_list[i].weight
        return total_weight

    @staticmethod
    def _check_duplicate_solutions(S1, S2):
        for i in range(0, len(S1)):
            if S1[i] != S2[i]:
                return False
        return True

    def _initial_population(self, population_size):
        population = []
        while len(population) < population_size:
            new_solution = self._create_rand_solution()
            if self._is_valid(new_solution) and self._is_unique_solution(new_solution, population):
                population.append(new_solution)
        return population

    def _is_unique_solution(self, new_solution, population):
        for existing_solution in population:
            if self._check_duplicate_solutions(new_solution, existing_solution):
                return False
        return True

    # Турнірна селекція: з популяції Р випадковим чином вибирається деяка
    # підмножина і батьком призначається найкраще рішення в P множині
    def _tournament_selection(self, curr_population):
        variant_1 = random.randint(0, len(curr_population) - 1)
        variant_2 = random.randint(0, len(curr_population) - 1)
        # обрахування придатності вибраних особин
        if self._totalCost(curr_population[variant_1]) > self._totalCost(curr_population[variant_2]):
            winner = curr_population[variant_1]
        else:
            winner = curr_population[variant_2]
        return winner

    # рівномірний кросиновер, кожен ген від батьків передається випадковим чином з ймовірністю 0,5.
    def _equal_crossover(self, p1, p2):
        child = []  # list with the genes of the child
        for gene1, gene2 in zip(p1, p2):
            prob = random.randint(0, 1)
            if prob < 0.5:
                child.append(gene1)
            else:
                child.append(gene2)

        if self._is_valid(child):
            return child
        else:
            return self._equal_crossover(p1, p2)

    @staticmethod
    def __swap(lst, index1, index2):
        lst[index1], lst[index2] = lst[index2], lst[index1]

    def _mutation(self, chromosome):
        temp = chromosome.copy()  # копія хромосоми
        mutation_index_1, mutation_index_2 = random.sample(range(0, len(chromosome)), 2)
        # обрано два випадкових індекси в хромосомі
        self.__swap(temp, mutation_index_1, mutation_index_2)
        if self._is_valid(temp):
            return temp
        else:
            return self._mutation(chromosome)

    def _create_generation(self, pop, mut_rate):
        new_gen = []
        for i in range(0, len(pop)):
            S1 = self._tournament_selection(pop)
            S2 = self._tournament_selection(pop)
            child = self._equal_crossover(S1, S2)
            if random.random() < mut_rate:
                child = self._mutation(child)
            # child = self.__greedy_improvement(child)
            new_gen.append(child)
        return new_gen

    def _goal_solution(self, generation):
        best = 0
        for i in range(0, len(generation)):
            temp = self._totalCost(generation[i])
            if temp > best:
                best = temp
        return best

