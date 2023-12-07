import random


def generate_random_float(start, end):
    return round(random.uniform(start, end), 2)


class ItemsGenerator:
    def __init__(self, file_name: str, min_w: int, max_w: int, min_c: int, max_c: int, numOfItems: int):
        self.__file = file_name
        self.__min_w = min_w
        self.__max_w = max_w
        self.__min_c = min_c
        self.__max_c = max_c
        self.__N = numOfItems

    def generateItems(self):
        data = []
        for i in range(self.__N):
            item_id = i
            weight = generate_random_float(self.__min_w, self.__max_w)
            cost = generate_random_float(self.__min_c, self.__max_c)
            data.append((item_id, weight, cost))

        # Write data to a file
        with open(self.__file, 'w') as file:
            for row in data:
                file.write(' '.join(map(str, row)) + '\n')

        print(f"File '{self.__file}' has been generated.")
