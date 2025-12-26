from dataclasses import dataclass
from typing import Dict, Any

import numpy as np

from .environment import Environment
from .layout import Layout
from ..utils.config import SimulationConfig


@dataclass
class SimulationSnapshot:
    frame: int
    positions: np.ndarray
    zone_counts: Dict[str, int]


class SimulationEngine:
    def __init__(self, layout: Layout, sim_cfg: SimulationConfig):
        self.layout = layout
        self.cfg = sim_cfg
        self.env = Environment.create_initial(layout, sim_cfg)
        self.frame = 0

    def update_positions(self, mode: str) -> None:
        positions = self.env.get_positions_array()

        if mode == "NORMAL":
            positions[:, 1] += 0.3
        else:
            # EVAC: move toward nearest exit center
            exit_targets = []
            for ex in self.layout.exits:
                r = ex.rect
                cx = r.x1 + (r.x2 - r.x1) / 2.0
                cy = r.y1 + (r.y2 - r.y1) / 2.0
                exit_targets.append([cx, cy])
            exit_targets = np.array(exit_targets, dtype=np.float32)

            for i in range(len(positions)):
                px, py = positions[i]
                dists = np.linalg.norm(exit_targets - np.array([px, py]), axis=1)
                nearest_exit = exit_targets[np.argmin(dists)]
                direction = nearest_exit - np.array([px, py])
                norm = np.linalg.norm(direction)
                if norm > 0:
                    direction = direction / norm
                positions[i] += direction * 1.5

        # Lateral jitter
        positions[:, 0] += np.random.uniform(-0.1, 0.1, size=len(positions))

        # Clamp
        stage = self.layout.stage.rect
        max_y = stage.y1 - 20
        positions[:, 1] = np.clip(
            positions[:, 1],
            self.cfg.top_ui_height + 60,
            max_y,
        )
        positions[:, 0] = np.clip(
            positions[:, 0],
            20,
            self.layout.width - self.cfg.right_margin - 20,
        )

        # Write back
        for i, agent in enumerate(self.env.agents):
            agent.x = float(positions[i, 0])
            agent.y = float(positions[i, 1])

    def step(self, mode: str) -> SimulationSnapshot:
        self.frame += 1
        self.update_positions(mode)
        positions = self.env.get_positions_array()

        # Zone counts will be computed in zone_risk, but we also return a simple count map.
        zone_counts: Dict[str, int] = {}
        for z in self.layout.zones:
            r = z.rect
            mask = (
                (positions[:, 0] >= r.x1)
                & (positions[:, 0] <= r.x2)
                & (positions[:, 1] >= r.y1)
                & (positions[:, 1] <= r.y2)
            )
            zone_counts[z.name.lower()] = int(np.sum(mask))

        return SimulationSnapshot(
            frame=self.frame,
            positions=positions,
            zone_counts=zone_counts,
        )

    def debug_info(self) -> Dict[str, Any]:
        return {
            "frame": self.frame,
            "num_agents": len(self.env.agents),
            "width": self.layout.width,
            "height": self.layout.height,
        }
