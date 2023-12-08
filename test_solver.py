import os
import unittest
from items import Item
from solver import KnapsackSolver


class MyTestCase(unittest.TestCase, KnapsackSolver):
    def setUp(self):
        self.solver = KnapsackSolver("test_file.txt", 50, 100, 200, 0.01, 1000)
        self.test_file = 'test_items.txt'

    def test_read_input(self):
        # Create a test file
        with open("test_file.txt", "w") as f:
            f.write("1 10 60\n2 20 100\n3 30 120\n")
        self.solver.read_input()
        # Check if items are read correctly
        self.assertEqual(len(self.solver.items_list), 3)
        self.assertEqual(self.solver.items_list[0].id, 1)
        self.assertEqual(self.solver.items_list[0].weight, 10)
        self.assertEqual(self.solver.items_list[0].value, 60)

        os.remove("test_file.txt")

    def test_create_rand_solution(self):
        solution = self.solver._create_rand_solution()
        self.assertEqual(len(solution), len(self.solver.items_list))
        self.assertTrue(all(i == 0 or i == 1 for i in solution))

    def test_create_random_solution(self):
        self.solver.items_list = [Item(0, 10, 20), Item(1, 15, 25)]
        solution = self.solver._create_rand_solution()
        self.assertEqual(len(solution), 2)

    def test_totalWeight(self):
        self.solver.items_list = [Item(0, 10, 20), Item(1, 15, 25)]
        weight = self.solver._totalWeight([1, 0])
        self.assertEqual(weight, 10)

    def test_check_duplicate_solutions(self):
        s1 = [1, 0, 1]
        s2 = [1, 1, 0]
        s3 = [1, 0, 1]
        self.assertTrue(self.solver._check_duplicate_solutions(s1, s3))
        self.assertFalse(self.solver._check_duplicate_solutions(s1, s2))

    def test_tournament_selection(self):
        # Create an instance of KnapsackSolver
        solver = KnapsackSolver("items_test.txt", 100, 10, 100, 0.1, 50)
        solver.find_solution()
        # Mock population for testing
        mock_population = [[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 1, 1]]
        # Test the _tournament_selection method
        winner = solver._tournament_selection(mock_population)
        self.assertTrue(winner in mock_population)

    def test_equal_crossover(self):
        # Create an instance of KnapsackSolver
        solver = KnapsackSolver("items_test.txt", 100, 10, 100, 0.1, 50)
        solver.find_solution()
        # Mock parent populations for testing
        parent1 = [0, 1, 0, 1]
        parent2 = [1, 0, 1, 0]
        # Test the _equal_crossover method
        child = solver._equal_crossover(parent1, parent2)
        self.assertEqual(len(child), len(parent1))
        self.assertTrue(all(gene in [0, 1] for gene in child))

    def test_mutation(self):
        self.solver.file = 'items_test.txt'  # Specify the correct file path for testing
        self.solver.read_input()
        # Mock chromosome for testing
        chromosome = [0, 1, 0, 1]
        mutated_chromosome = self.solver._mutation(chromosome)
        # Ensure the mutation happened (chromosome is not equal to mutated_chromosome)
        self.assertNotEqual(chromosome, mutated_chromosome)
        # Ensure the mutated chromosome is valid
        self.assertTrue(self.solver._is_valid(mutated_chromosome))

    def test_create_generation(self):
        # Ensure items_list is populated
        self.solver.file = 'items_test.txt'
        self.solver.read_input()
        # Mock population for testing
        mock_population = [[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 1, 1]]
        mock_mut_rate = 0.1
        # Test the _create_generation method
        new_gen = self.solver._create_generation(mock_population, mock_mut_rate)
        # Ensure the new generation has the same length as the original population
        self.assertEqual(len(new_gen), len(mock_population))
        # Ensure each chromosome in the new generation is valid
        for chromosome in new_gen:
            self.assertTrue(self.solver._is_valid(chromosome))

    def test_goal_solution(self):
        self.solver.file = 'items_test.txt'
        self.solver.read_input()
        # Mock generation for testing
        mock_generation = [[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 1, 1]]
        # Test the _goal_solution method
        best_solution = self.solver._goal_solution(mock_generation)
        # Mock total costs for each chromosome in the generation
        total_costs = [self.solver._totalCost(chromosome) for chromosome in mock_generation]
        # Ensure the best_solution matches the maximum total cost
        self.assertEqual(best_solution, max(total_costs))

    # def tearDown(self):
    #     # Clean up by removing the temporary file
    #     if os.path.exists(self.test_file):
    #         os.remove(self.test_file)
    #
    # def test_generate_items(self):
    #     # Create an instance of ItemsGenerator for testing
    #     generator = ItemsGenerator(self.test_file, 1, 10, 5, 20, 3)
    #
    #     # Test the generateItems method
    #     generator.generateItems()
    #
    #     # Check if the file has been generated
    #     self.assertTrue(os.path.exists(self.test_file))
    #
    #     # Read the content of the file and check if it has the expected number of lines
    #     with open(self.test_file, 'r') as file:
    #         lines = file.readlines()
    #         self.assertEqual(len(lines), 3)  # Assuming 3 items were generated
    #
    #     # Check if the content of each line is in the expected format
    #     for line in lines:
    #         parts = line.strip().split()
    #         self.assertEqual(len(parts), 3)  # Assuming each line has three values
    #         item_id, weight, cost = map(float, parts)
    #         self.assertIsInstance(item_id, float)
    #         self.assertIsInstance(weight, float)
    #         self.assertIsInstance(cost, float)

if __name__ == '__main__':
    unittest.main()
