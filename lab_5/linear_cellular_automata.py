from random import randrange, randint
from copy import deepcopy


class LinearCellularAutomata:
    def __init__(self):
        self.__length = randint(3, 30)
        self.__main_array = self.__generate_random_array()
        self.__helper_array = deepcopy(self.__main_array)

    @property
    def main_array(self):
        return self.__main_array

    def __generate_random_array(self):
        return [randrange(1, self.__length, 1) for _ in range(self.__length)]

    def __calculate(self, i: int):
        if i == 1:
            first_item = self.__helper_array[self.__length - 1]
        else:
            first_item = self.__helper_array[i - 1]
        if i == self.__length - 1:
            end_item = self.__helper_array[0]
        else:
            end_item = self.__helper_array[i + 1]
        return first_item * self.__helper_array[i] + end_item

    def __replace(self, i: int, new_value: float):
        self.__main_array[i] = new_value

    def run(self):
        for i in range(self.__length):
            self.__replace(i, self.__calculate(i))
