from typing import List, Tuple
from random import uniform, randint
from bitstring import BitArray
from math import cos, pi


class GeneticAlgorithm:
    def __init__(self,
                 iterations: int = 10,
                 population_size: int = 5,
                 bit_length: int = 32,
                 mutants: int = 2,
                 precision: int = 2):
        self.__iterations = iterations
        self.__population_size = population_size
        self.__bit_length = bit_length
        self.__mutants = mutants
        self.__precision = precision
        self.__population = [[], []]
        self.generate()

    @property
    def iterations(self) -> int:
        return self.__iterations

    @property
    def population_size(self) -> int:
        return self.__population_size

    @property
    def mutants_count(self) -> int:
        return self.__mutants

    @property
    def population(self) -> List[List[str]]:
        return self.__population

    def __convert_float_to_binary(self, number: float) -> str:
        return BitArray(float=number, length=self.__bit_length).bin

    @staticmethod
    def convert_binary_to_float(binary: str) -> float:
        return BitArray(bin=binary).float

    def __get_rand_values(self) -> List[int]:
        rand_values = []
        for i in range(self.__population_size):
            rand_values.append(uniform(-5.12, 5.12))
        return rand_values

    def __generate_binary(self, rand_values: List[List[str]]) -> List[str]:
        population = []
        for rand_value in rand_values:
            population.append(self.__convert_float_to_binary(rand_value))
        return population

    def generate(self) -> List[List[str]]:
        self.__population = [
            self.__generate_binary(self.__get_rand_values()),
            self.__generate_binary(self.__get_rand_values())
        ]

    def __calculate_fitness_function(self) -> List[float]:
        results = []
        for i in range(len(self.__population[0])):
            x1 = round(self.convert_binary_to_float(self.__population[0][i]),
                       self.__precision)
            x2 = round(self.convert_binary_to_float(self.__population[1][i]),
                       self.__precision)
            results.append(
                round(
                    20 + x1**2 + x2**2 - 10 * cos(2 * pi * x1) -
                    10 * cos(2 * pi * x2), self.__precision))
        return results

    def __get_average_population(self) -> float:
        values = []
        for row in self.__population:
            for binary_value in row:
                values.append(self.convert_binary_to_float(binary_value))
        return sum(values) / len(values)

    def __get_parents(self, ff_result: List[float],
                      average_population: float) -> List[str]:
        parents = [[], []]
        for i in range(len(self.__population[0])):
            if ff_result[i] >= average_population:
                parents[0].append(self.__population[0][i])
                parents[1].append(self.__population[1][i])
        return parents

    def __check_constraints(self, binary: str) -> bool:
        return -5.12 <= self.convert_binary_to_float(binary) <= 5.12

    def __cross(self, parents: List[str]) -> List[str]:
        start = randint(0, self.__bit_length // 2)
        end = randint(start, self.__bit_length)
        children = [[], []]
        for i in range(len(parents[0])):
            first_parent = parents[0][i]
            second_parent = parents[1][i]
            first_child = first_parent[0:start] + second_parent[start:end] \
              + second_parent[end:self.__bit_length]
            second_child = second_parent[0:start] + first_parent[start:end] \
              + second_parent[end:self.__bit_length]
            if self.__check_constraints(first_child) \
            and self.__check_constraints(second_child):
                children[0].append(first_child)
                children[1].append(second_child)
        self.__population[0].extend(children[0])
        self.__population[1].extend(children[1])
        return children

    def __mutate(self) -> None:
        for i in range(self.__mutants):
            x = randint(0, 1)
            y = randint(0, self.__population_size - 1)
            current = self.__population[x][y]
            average_index = len(self.__population) // 2
            mutant = current[average_index:self.__bit_length] \
              + current[0:average_index]
            if self.__check_constraints(mutant):
                self.__population[x][y] = mutant

    def __select(self, ff_results: List[float]) -> List[float]:
        """Selection mechanism."""
        for i in range(len(self.__population[0])):
            if len(self.__population[0]) == self.__population_size:
                break
            if self.__population[0][i] in self.__population[0][i:] \
              and self.__population[1][i] in self.__population[1][i:]:
                del self.__population[0][i]
                del self.__population[1][i]
                del ff_results[i]
        sorted_ff_results = sorted(ff_results, reverse=True)
        for i, ff_result in enumerate(sorted_ff_results):
            index = ff_results.index(ff_result)
            if len(self.__population[0]) != self.__population_size:
                del self.__population[0][index]
                del self.__population[1][index]
            else:
                self.__population[0][i], self.__population[0][index] = self.__population[0][index], \
                self.__population[0][i]
                self.__population[1][i], self.__population[1][index] = self.__population[1][index], \
                self.__population[1][i]
        return sorted_ff_results

    @staticmethod
    def check_finish(previous_ff_results: List[float],
                       ff_result: List[float]) -> bool:
        return len(
            previous_ff_results) > 0 and max(previous_ff_results) == max(ff_result)

    def start_iteration(self,
                        previous_ff_result: List[float] = []) -> List[float]:
        ff_results = self.__calculate_fitness_function()  # fitness function results
        if self.check_finish(previous_ff_result, ff_results):
            return ff_results
        parents: List[str] = self.__get_parents(
            ff_results, self.__get_average_population())
        self.__cross(parents)
        self.__mutate()  # apply the mutation
        ff_results = self.__calculate_fitness_function()  # fitness function result
        ff_results = self.__select(ff_results)
        return ff_results

    def convert_result_to_tuple(self, previous_ff_results: List[float]) -> Tuple[float, float, float]:
        result = max(previous_ff_results)
        index = previous_ff_results.index(result)
        return (round(self.convert_binary_to_float(self.__population[0][index]),
                      self.__precision),
                round(self.convert_binary_to_float(self.__population[1][index]),
                      self.__precision), result)
                      
    def run(self) -> Tuple[float]:
        """"Entry point."""
        previous_ff_results = []
        for i in range(self.__iterations):  # main cycle
            ff_results = self.start_iteration(previous_ff_results)
            if self.check_finish(previous_ff_results, ff_results):
                break
            previous_ff_results = ff_results
        return self.convert_result_to_tuple(previous_ff_results)
