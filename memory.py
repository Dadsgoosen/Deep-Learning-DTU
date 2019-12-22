from typing import Tuple, List

import numpy.random as rand
import numpy as np


class ReplayMemory:

    def __init__(self, capacity: int):
        self.capacity: int = capacity
        self.throw_memory: List[float] = []
        self.force_memory: List[float] = []
        self.force_result: List[float] = []
        self.means: List[float] = []
        self.current_mean: float = 1000000
        self.length = 0

    def push(self, throw: float, force: float, result: float) -> None:
        self.__prioritize_full(result)
        self.throw_memory.append(throw)
        self.force_memory.append(force)
        self.force_result.append(result)
        self.length += 1
        self.current_mean = np.array(self.force_result).mean()
        self.means.append(self.current_mean)

    def __prioritize_full(self, result: float) -> bool:
        if self.length < self.capacity or result < self.current_mean:
            return False

        max_indice = np.argmax(np.array(self.force_result))

        if isinstance(max_indice, (np.ndarray, list)):
            max_indice = max_indice[0]

        self.throw_memory.pop(max_indice)
        self.force_memory.pop(max_indice)
        self.force_result.pop(max_indice)

        return True
