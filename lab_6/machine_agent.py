from random import randint
from math import ceil


class MachineAgent:
    def __init__(self, size: int = 5, step: int = 1):
        self.__size = size  # N
        self.__step = step
        self.__current_position = 0
        self.__array = [randint(0, 1) for _ in range(self.__size)]
        self.__apples_count = len([item for item in self.__array if item == 1])
        self.__scores = 0
        self.__apples_remainder = self.__apples_count
        self.__moves_count = ceil(self.size / abs(self.__step))  # N
        self.__moves_made_count = 0  # S
        self.__fitness_function = None

    @property
    def size(self):
        return self.__size

    @property
    def step(self):
        return self.__step

    @property
    def array(self):
        return self.__array

    @property
    def fitness_function(self):
        return self.__fitness_function

    @property
    def moves_made_count(self):
        return self.__moves_made_count

    @property
    def scores(self):
        return self.__scores

    def __eat_apple(self):
        self.__scores += 1
        self.__apples_remainder -= 1

    def __move(self):
        if self.__array[self.__current_position]:
            self.__eat_apple()
        if self.__current_position == self.__size - 1:
            self.__step *= -1
        elif self.__current_position == 0 and self.__step == -abs(self.__step):
            self.__step = abs(self.__step)
        self.__current_position += self.__step

    def __calculate_fitness_function(self):
        self.__fitness_function = self.__moves_made_count / self.__moves_count

    def __eq__(self, other):
        return self.__fitness_function == other.__fitness_function

    def __lt__(self, other):
        return self.__fitness_function < other.__fitness_function

    def run(self):
        self.__scores = 0
        self.__apples_remainder = self.__apples_count
        self.__moves_made_count = 0
        while True:
            self.__move()
            if self.__apples_remainder > 0:
                self.__moves_made_count += 1
            else:
                break
        self.__calculate_fitness_function()
