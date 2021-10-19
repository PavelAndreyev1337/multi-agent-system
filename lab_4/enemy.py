from typing import List
from random import choices, uniform


class Enemy:
    def __init__(self, available_moves: List[int], a1: float, a2: float,
                 evaluation_threshold: float):
        self.__available_moves = list(set(available_moves))
        self.__evaluation_threshold = evaluation_threshold
        self.__a1 = a1
        self.__a2 = a2
        self.__probability_distribution = [
            self.__a1, self.__a2, 1 - self.__a1 - self.__a2
        ]
        self.__moves = []

    @property
    def available_moves(self) -> List[int]:
        return self.__available_moves

    @property
    def moves(self) -> List[int]:
        return self.__moves

    def choice_move(self, forecasting_estimate: float) -> str:
        """The enemy agent generates random move."""
        if self.__evaluation_threshold == forecasting_estimate:  # The enemy changes the probability distribution.
            residual_probability = 1.0
            for i in range(len(self.__available_moves)):
                self.__probability_distribution[i] = uniform(
                    0.0, residual_probability)
                if self.__probability_distribution[i] > residual_probability:
                    residual_probability = 0
                else:
                    residual_probability -= self.__probability_distribution[i]
        move = choices(self.__available_moves,
                       weights=self.__probability_distribution,
                       k=1)[0]
        self.__moves.append(move)
        return str(move)
