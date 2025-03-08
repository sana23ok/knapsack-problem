import unittest
import os
from items_generator import generate_random_num, ItemsGenerator


class TestItemsGenerator(unittest.TestCase):
    def setUp(self):
        self.file_name = "test_items.txt"
        self.min_w = 1
        self.max_w = 10
        self.min_c = 1
        self.max_c = 10
        self.numOfItems = 5
        self.generator = ItemsGenerator(self.file_name, self.min_w, self.max_w, self.min_c, self.max_c, self.numOfItems)

    def test_generate_random_float(self):
        random_float = generate_random_num(self.min_w, self.max_w)
        self.assertTrue(self.min_w <= random_float <= self.max_w)

    def test_generateItems(self):
        self.generator.generate_items()
        self.assertTrue(os.path.exists(self.file_name))
        with open(self.file_name, 'r') as file:
            lines = file.readlines()
            self.assertEqual(len(lines), self.numOfItems)
            for i, line in enumerate(lines):
                item_id, weight, cost = map(float, line.split())
                self.assertEqual(item_id, i)
                self.assertTrue(self.min_w <= weight <= self.max_w)
                self.assertTrue(self.min_c <= cost <= self.max_c)
        os.remove(self.file_name)


if __name__ == "__main__":
    unittest.main()
