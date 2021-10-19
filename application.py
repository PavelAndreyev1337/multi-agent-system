from lab_1.genetic_algorithm import GeneticAlgorithm
from lab_2.parallel_genetic_algorithm import ParallelGeneticAlgorithm
from lab_3.machine import Machine
from lab_4.modeling import Modeling
from lab_5.linear_cellular_automata import LinearCellularAutomata
from lab_5.two_dimensional_cellular_automata import TwoDimensionalCellularAutomata
from lab_6.machine_genetic_algorithm import MachineGeneticAlgorithm
from time import time


class Application:
    def __init__(self):
        self._genetic_algorithm = GeneticAlgorithm()
        self._parallel_genetic_algorithm = ParallelGeneticAlgorithm()
        self._machine = Machine()
        self.__modeling = None
        self.__linear_cellular_automata = LinearCellularAutomata()
        self.__two_dimensional_cellular_automata = TwoDimensionalCellularAutomata(
        )
        self.__machine_genetic_algorithm = MachineGeneticAlgorithm()

    def __print_genetic_algorithm(self, x1, x2, f, end_time, number=1):
        print(f"\nLab {number}")
        print(f"x1 = {x1} x2 = {x2} F(x1,x2) = {f} Time = {end_time}")

    def __run_machine(self):
        print(f"\nLab 3: \n{self._machine.run()}")

    def __model_interaction_under_uncertainty(self):
        steps_number = int(input("\nLab 4:\n Кількість кроків моделювання:"))
        a1 = float(input("a1: "))
        a2 = float(input("a2:"))
        evaluation_threshold = float(input("Поріг оцінки:"))
        self.__modeling = Modeling(steps_number, a1, a2, evaluation_threshold)
        self.__modeling.run()
        for title in self.__modeling.titles:
            print(title, end=" | ")
        print()
        for result in self.__modeling.results:
            for column in result:
                print(column, end=" | ")
            print()
        self.__modeling.export_csv()

    def __run_cellular_automata(self):
        print("\nLab 5:")
        print(self.__linear_cellular_automata.main_array)
        self.__linear_cellular_automata.run()
        print(self.__linear_cellular_automata.main_array, end="\n")
        print(self.__two_dimensional_cellular_automata.main_array)
        self.__two_dimensional_cellular_automata.run()
        print(self.__two_dimensional_cellular_automata.main_array)

    def __run_machine_genetic_algorithm(self):
        print("\nLab 6:")
        result = self.__machine_genetic_algorithm.run()
        print(f"Число кроків: {result.moves_made_count}")
        print(f"Число яблук, з’їдених автоматом : {result.scores}")

    def run(self):
        start_time = time()
        for i, genetic_algorithm in enumerate(
            [self._genetic_algorithm, self._parallel_genetic_algorithm]):
            self.__print_genetic_algorithm(*genetic_algorithm.run(),
                                           time() - start_time, i + 1)
        self.__run_machine()
        self.__model_interaction_under_uncertainty()
        self.__run_cellular_automata()
        self.__run_machine_genetic_algorithm()
