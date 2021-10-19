from typing import Tuple, List
from .thread_subpopulation import GeneticAlgorithm, ThreadSubpopulation
from random import randint
from copy import deepcopy

class ParallelGeneticAlgorithm:
    def __init__(self,
                 iterations: int = 10,
                 subpopulation_count: int = 5,
                 subpopulation_size: int = 5,
                 bit_length: int = 32,
                 mutants_count: int = 1,
                 precision: int = 2):
        self.__iterations = iterations
        self.__precision = precision
        self.__subpopulation_size = subpopulation_size
        self.__subpopulations = []
        self.__subpopulation_count = subpopulation_count
        for _ in range(self.__subpopulation_count):
            self.__subpopulations.append(
                GeneticAlgorithm(iterations, self.__subpopulation_size,
                                 bit_length, mutants_count, self.__precision))

    def __get_rand_subpopulations_index(self):
        return randint(0, len(self.__subpopulations) - 1)

    def __migrate(self, destination: GeneticAlgorithm, source: List[GeneticAlgorithm]):
        rand_index = randint(0, len(source.population[0]) - 1)
        destination.population[0].append(source.population[0][rand_index])
        destination.population[1].append(source.population[1][rand_index])
        del source.population[0][rand_index]
        del source.population[1][rand_index]

    def __add_immigrants(self):
        count = randint(0, len(self.__subpopulations) - 1)
        for i in range(count):
            rand_index1 = self.__get_rand_subpopulations_index()
            rand_index2 = self.__get_rand_subpopulations_index()
            if rand_index1 != rand_index2:
                self.__migrate(self.__subpopulations[rand_index1], self.__subpopulations[rand_index2])
                self.__migrate(self.__subpopulations[rand_index2], self.__subpopulations[rand_index1])


    def convert_result_to_tuple(self, previous_ff_results: List[float]) -> Tuple[float, float, float]:
        result = max(previous_ff_results)
        index = previous_ff_results.index(result)
        population = [[], []]
        for subpopulation in self.__subpopulations:
            population[0].extend(subpopulation.population[0])
            population[1].extend(subpopulation.population[1])
        return (round(GeneticAlgorithm.convert_binary_to_float(population[0][index]),
                      self.__precision),
                round(GeneticAlgorithm.convert_binary_to_float(population[1][index]),
                      self.__precision), result)

    def run(self) -> Tuple[float]:
        threads = []
        previous_ff_results = []
        current_ff_results = []
        for i in range(self.__iterations):
            current_ff_results = []
            for i, subpopulation in enumerate(self.__subpopulations):
                thread = ThreadSubpopulation(subpopulation,
                                             deepcopy(previous_ff_results))
                threads.append(thread)
                thread.start()
            for thread in threads:
                current_ff_results.extend(thread.join(
                ))  # the results of the fitness function from the thread'
                current_ff_results = current_ff_results[0:self.__subpopulation_size * self.__subpopulation_count]
            if GeneticAlgorithm.check_finish(previous_ff_results,
                                             current_ff_results):
                previous_ff_results = current_ff_results
                break
            elif i != self.__iterations - 1:
                self.__add_immigrants()
            previous_ff_results = current_ff_results
        return self.convert_result_to_tuple(previous_ff_results)
