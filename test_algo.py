import random
import items
import matplotlib.pyplot as plt

file_name = "items.txt"
carrier_limit = 150
population_size = 100
generation_size = 100
mutation_rate = 0.05

item_list = []
with open(file_name, "r") as f:
    for line in f:  # check each line
        new_line = line.strip()  # remove spaces at the beginning and the end if they are available
        new_line = new_line.split(" ")  # split a string into a list
        # w --> weight | v --> value
        id, w, v = new_line[0], new_line[1], new_line[2]  # check dataset file to see why id,w,v = 0,1,2
        new_item = items.Item(int(id), float(w), float(v))
        item_list.append(new_item)


def create_random_solution(i_list):
    solution = []
    for i in range(0, len(i_list)):
        solution.append(random.randint(0, 1))
    return solution


def valid_solution(i_list, s_list, limit):
    total_weight = 0
    for i in range(0, len(s_list)):
        if s_list[i] == 1:
            total_weight += i_list[i].weight
        if total_weight > limit:
            return False
    return True


def calculate_value(i_list, s_list):
    total_value = 0
    for i in range(0, len(s_list)):
        if s_list[i] == 1:
            total_value += i_list[i].value
    return total_value


def check_duplicate_solutions(s_1, s_2):
    for i in range(0, len(s_1)):
        if s_1[i] != s_2[i]:
            return False
    return True


def initial_population(pop_size, i_list, w_limit):
    population = []
    i = 0
    while i < pop_size:
        new_solution = create_random_solution(i_list)
        if valid_solution(i_list, new_solution, w_limit):
            if len(population) == 0:
                population.append(new_solution)
                i += 1
            else:
                skip = False
                for j in range(0, len(population)):
                    if check_duplicate_solutions(new_solution, population[j]):
                        skip = True
                        continue
                if not skip:
                    population.append(new_solution)
                    i += 1
    return population


def tournament_selection(pop):
    ticket_1 = random.randint(0, len(pop) - 1)
    ticket_2 = random.randint(0, len(pop) - 1)
    if calculate_value(item_list, pop[ticket_1]) > calculate_value(item_list, pop[ticket_2]):
        winner = pop[ticket_1]
    else:
        winner = pop[ticket_2]
    return winner


def crossover(p_1, p_2):
    break_point = random.randint(0, len(p_1))
    first_part = p_1[:break_point]
    second_part = p_2[break_point:]
    child = first_part + second_part
    if valid_solution(item_list, child, carrier_limit):
        return child
    else:
        return crossover(p_1, p_2)


def mutation(chromosome):
    temp = chromosome.copy()  # Create a copy of the chromosome
    mutation_index_1, mutation_index_2 = random.sample(range(0, len(chromosome)), 2)
    temp[mutation_index_1], temp[mutation_index_2] = temp[mutation_index_2], temp[mutation_index_1]

    if valid_solution(item_list, temp, carrier_limit):
        return temp
    else:
        return mutation(chromosome)

# def mutation(chromosome):
#     temp = chromosome
#     mutation_index_1, mutation_index_2 = random.sample(range(0, len(chromosome)), 2)
#     temp[mutation_index_1], temp[mutation_index_2] = temp[mutation_index_2], temp[mutation_index_1]
#
#     if valid_solution(item_list, temp, carrier_limit):
#         return temp
#     else:
#         return mutation(chromosome)


def create_generation(pop, mut_rate):
    new_gen = []
    for i in range(0, len(pop)):
        parent_1 = tournament_selection(pop)
        parent_2 = tournament_selection(pop)
        child = crossover(parent_1, parent_2)
        if random.random() < mut_rate:
            child = mutation(child)
        new_gen.append(child)
    return new_gen


def best_solution(generation, i_list):
    best = 0
    for i in range(0, len(generation)):
        temp = calculate_value(i_list, generation[i])
        if temp > best:
            best = temp
    return best


value_list = []


def genetic_algorithm(c_limit, p_size, gen_size, mutation_rate, i_list):
    pop = initial_population(p_size, i_list, c_limit)
    for i in range(0, gen_size):
        pop = create_generation(pop, mutation_rate)
        print(pop[0])

        print("value --> ", calculate_value(i_list, pop[0]))
        value_list.append(best_solution(pop, i_list))
    return pop, value_list


latest_pop, v_list = genetic_algorithm(c_limit=carrier_limit,
                                       p_size=population_size,
                                       gen_size=generation_size,
                                       mutation_rate=mutation_rate,
                                       i_list=item_list)
plt.plot(v_list)
plt.xlabel('generations')
plt.ylabel('values')
plt.title("Values of the solutions during the generations")
plt.show()
