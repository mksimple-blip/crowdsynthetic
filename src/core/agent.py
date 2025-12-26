from dataclasses import dataclass
import numpy as np


@dataclass
class Agent:
    x: float
    y: float

    def position(self) -> np.ndarray:
        return np.array([self.x, self.y], dtype=np.float32)

    def move(self, delta: np.ndarray) -> None:
        self.x += float(delta[0])
        self.y += float(delta[1])
