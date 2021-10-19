from threading import Thread
from lab_1.genetic_algorithm import GeneticAlgorithm
from typing import List


class ThreadSubpopulation(Thread):
    def __init__(self,
                 subpopulation: GeneticAlgorithm,
                 previous_ff_result: List[float] = []):
        super().__init__()
        self.__subpopulation = subpopulation
        self.__previous_ff_result = previous_ff_result

    def run(self):
        self.__previous_ff_result = self.__subpopulation.start_iteration(self.__previous_ff_result)

    def join(self):
        Thread.join(self)
        return self.__previous_ff_result
