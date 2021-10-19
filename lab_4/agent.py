from typing import List, Dict
from random import choice, choices
from copy import deepcopy


class Agent:
    def __init__(self, available_moves: List[int],
                 evaluation_threshold: float):
        self.__available_moves = list(set(available_moves))
        self.__evaluation_threshold = evaluation_threshold
        self.__predicted_moves = []
        self.__all_moves = []  # [{N1, N2, N3},...]
        self.__moves = {}
        self.__init_moves(self.__moves)
        self.__probability_distribution = []
        self.__successful_guesses_count = 0
        self.__forecasting_estimates = []

    @property
    def predicted_moves(self) -> List[int]:
        return self.__predicted_moves

    @property
    def forecasting_estimates(self) -> List[float]:
        return self.__forecasting_estimates

    @property
    def all_moves(self) -> Dict[str, int]:
        return self.__all_moves

    def __init_moves(self, moves):
        for available_move in self.__available_moves:
            moves[str(available_move)] = 0

    def __append_move_to_all_moves(self, enemy_move):
        if self.__all_moves:
            self.__all_moves.append(deepcopy(self.__all_moves[-1]))
        else:
            self.__all_moves.append({})
            self.__init_moves(self.__all_moves[-1])
        self.__all_moves[-1][enemy_move] += 1

    def __reset_moves(self):
        self.__init_moves(self.__moves)

    def get_last_forecasting_estimate(self):
        if self.__forecasting_estimates:
            return self.__forecasting_estimates[-1]
        return None

    def predict_enemy_move(self) -> int:
        """The agent predicts the enemy move."""
        if len(self.__probability_distribution) == len(self.__available_moves):
            predicted_move = choices(self.__available_moves,
                                     weights=self.__probability_distribution,
                                     k=1)[0]
        else:
            predicted_move = choice(self.__available_moves)
        self.__predicted_moves.append(predicted_move)
        return predicted_move

    def evaluate_predictions(self, enemy_move: str) -> float:
        """The agent evaluates his predictions."""
        self.__moves[enemy_move] += 1
        self.__append_move_to_all_moves(enemy_move)
        moves_count = sum(self.__moves.values())
        for move, count in self.__moves.items():
            probability = count / moves_count
            if len(self.__probability_distribution) == len(
                    self.__available_moves):
                self.__probability_distribution[int(move) - 1] = probability
            else:
                self.__probability_distribution.append(probability)
        if enemy_move == str(self.__predicted_moves[-1]):
            self.__successful_guesses_count += 1
        forecasting_estimate = self.__successful_guesses_count / len(
            self.__predicted_moves)
        self.__forecasting_estimates.append(forecasting_estimate)
        if self.__evaluation_threshold == forecasting_estimate:
            self.__probability_distribution = []
            self.__reset_moves()
        return forecasting_estimate
