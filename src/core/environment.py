from dataclasses import dataclass
from typing import List

import numpy as np

from .agent import Agent
from .layout import Layout
from ..utils.config import SimulationConfig


@dataclass
class Environment:
    layout: Layout
    agents: List[Agent]

    @classmethod
    def create_initial(cls, layout: Layout, sim_cfg: SimulationConfig) -> "Environment":
        # Equivalent to your init_simulation positions area
        positions = np.random.randint(
            low=[40, sim_cfg.top_ui_height + 60],
            high=[layout.width - sim_cfg.right_margin - 40, layout.height - 160],
            size=(sim_cfg.num_people, 2),
        ).astype(np.float32)

        agents = [Agent(x=float(p[0]), y=float(p[1])) for p in positions]
        return cls(layout=layout, agents=agents)

    def get_positions_array(self) -> np.ndarray:
        return np.array([[a.x, a.y] for a in self.agents], dtype=np.float32)
