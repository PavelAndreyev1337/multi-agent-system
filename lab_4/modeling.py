from .agent import Agent
from .enemy import Enemy
from csv import writer


class Modeling:
    def __init__(self,
                 steps_number: int = 200,
                 a1: float = 0.15,
                 a2: float = 0.75,
                 evaluation_threshold: float = 0.6):
        self.__steps_number = steps_number
        self.__a1 = a1
        self.__a2 = a2
        self.__evaluation_threshold = evaluation_threshold
        self.__available_moves = range(1, 4)
        self.__agent = Agent(self.__available_moves,
                             self.__evaluation_threshold)
        self.__enemy = Enemy(self.__available_moves, self.__a1, self.__a2,
                             self.__evaluation_threshold)
        self.__titles = [
            "Номер кроку", "Хід", "Прогноз", "N1", "N2", "N3", "Оцінка"
        ]
        self.__results = []

    @property
    def titles(self):
        return self.__titles

    @property
    def results(self):
        for i, move in enumerate(self.__enemy.moves):
            result = [
                i + 1,
                move,
                round(self.__agent.predicted_moves[i], 2),
            ]
            result.extend(self.__agent.all_moves[i].values())
            result.append(round(self.__agent.forecasting_estimates[i], 2))
            self.__results.append(result)
        return self.__results

    def run(self):
        for i in range(self.__steps_number):
            self.__agent.predict_enemy_move()
            self.__agent.evaluate_predictions(
                self.__enemy.choice_move(
                    self.__agent.get_last_forecasting_estimate()))

    def export_csv(self):
        with open("lab_4.csv", "w", encoding='utf-8', newline='') as file:
            csv_writer = writer(file)
            csv_writer.writerow(self.__titles)
            for result in self.results:
                csv_writer.writerow(result)
