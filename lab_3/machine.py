from random import randint
from typing import List


class Machine:

    ACTIONS = ["move left", "move right"]

    def __init__(self):
        self._positions_count = 0
        self._x = []  # alphabet of inputs
        self._states_count = 0
        self._s = []  # alphabet of states
        self._s_index = None  # current s index
        self._history = ""
        self._initialize_attributes()

    def _initialize_attributes(self):
        self._positions_count = randint(2, 10)
        self._x = self._generate_binary_list(self._positions_count)
        self._states_count = randint(1, 10)
        self._s = self._generate_binary_list(self._states_count)
        self._s_index = 0
        self._history = ""

    @property
    def history(self) -> str:
        return self._history

    def _move_left(self) -> None:
        if self._s_index == 0:
            self._s_index = self._states_count - 1
        else:
            self._s_index -= 1

    def _move_right(self) -> None:
        if self._s_index == self._states_count - 1:
            self._s_index = 0
        else:
            self._s_index += 1

    def _generate_binary_list(self, size: int) -> List[int]:
        return [randint(0, 1) for _ in range(size)]

    def _calculate_xor(self, x: int, s: int) -> int:
        return x ^ s

    def _move(self, current_output: int) -> int:
        if current_output == 0:
            self._move_left()
            return Machine.ACTIONS[0]
        elif current_output == 1:
            self._move_right()
            return Machine.ACTIONS[1]

    def _append_history(self, i: int, x: int, previous_s_index: int,
                        move: str) -> str:
        self._history += f"x{i}={x} s{previous_s_index}={self._s[previous_s_index]} {move}\n"

    def _store_to_txt(self) -> None:
        with open("lab_3.txt", "w") as file:
            file.write(self._history)

    def run(self) -> str:
        self._initialize_attributes()
        for i, x in enumerate(self._x):
            self._append_history(
                i, x, self._s_index,
                self._move(self._calculate_xor(x, self._s[self._s_index])))
        self._store_to_txt()
        return self._history
