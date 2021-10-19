from random import randrange, randint
from copy import deepcopy


class TwoDimensionalCellularAutomata:
    def __init__(self):
        self.__size = randint(3, 5)
        self.__main_array = []
        self.__generate_random_array()
        self.__helper_array = deepcopy(self.__main_array)

    @property
    def main_array(self):
        return self.__main_array

    def __generate_random_array(self):
        for i in range(self.__size):
            self.__main_array.append(
                [randrange(1, self.__size, 1) for _ in range(self.__size)])

    def __calculate(self, i: int, j: int):
        if i == 1:
            top_item = self.__helper_array[self.__size - 1][j]
        else:
            top_item = self.__helper_array[i - 1][j]
        if j == self.__size - 1:
            right_item = self.__helper_array[i][0]
        else:
            right_item = self.__helper_array[i][j + 1]
        if i == self.__size - 1:
            bottom_item = self.__helper_array[0][j]
        else:
            bottom_item = self.__helper_array[i + 1][j]
        if j == 0:
            left_item = self.__helper_array[i][self.__size - 1]
        else:
            left_item = self.__helper_array[i][j - 1]
        return top_item * self.__helper_array[i][j] + right_item - bottom_item / left_item

    def __replace(self, i: int, j: int, new_value: float):
        self.__main_array[i][j] = new_value

    def run(self):
        for i in range(self.__size):
            for j in range(self.__size):
                self.__replace(i, j, self.__calculate(i, j))
