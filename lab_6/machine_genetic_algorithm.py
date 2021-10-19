from random import randint, choices, choice
from .machine_agent import MachineAgent


class MachineGeneticAlgorithm:
    def __init__(self,
                 epochs: int = 5,
                 population_size: int = 20,
                 parents_count: int = 5):
        self.__epochs = epochs
        self.__population_size = population_size
        self.__population = [
            MachineAgent() for _ in range(self.__population_size)
        ]
        self.__parents_count = parents_count

    def __run_machine_agents(self):
        for machineAgent in self.__population:
            machineAgent.run()

    def __get_fitness_functions(self):
        return [
            machineAgent.fitness_function for machineAgent in self.__population
        ]

    def __use_roulette_method(self):
        fitness_functions = self.__get_fitness_functions()
        fitness_functions_sum = sum(fitness_functions)
        probabilities = []
        for fitness_function in fitness_functions:
            if fitness_functions_sum:
                probabilities.append(fitness_function / fitness_functions_sum)
            else:
                probabilities.append(0)
        return choices(self.__population, weights=probabilities, k=3)

    def __cross(self, first_parents, second_parents):
        children = []
        for i, machine_agent in enumerate(first_parents):
            random_position = randint(0, machine_agent.size - 2)
            children.extend(first_parents[:random_position] +
                            second_parents[random_position:])
            children.extend(second_parents[:random_position] +
                            first_parents[random_position:])
        return children

    def __mutate(self):
        machime_agent = choice(self.__population)
        machime_agent.array[randint(0, machime_agent.size - 1)] = randint(0, 1)

    def __select(self):
        self.__population = sorted(self.__population,
                                   reverse=True)[:self.__population_size - 1]

    def run(self):
        for _ in range(self.__epochs):
            self.__run_machine_agents()
            self.__population.extend(
                self.__cross(self.__use_roulette_method(),
                             self.__use_roulette_method()))
            self.__mutate()
            self.__select()
        return self.__population[0]
