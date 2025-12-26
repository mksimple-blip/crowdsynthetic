from dataclasses import dataclass
from typing import Dict

import numpy as np

from ..core.layout import Layout, Zone
from ..utils.config import RiskConfig


@dataclass
class ZoneMetrics:
    count: int
    capacity: int
    density_ratio: float  # 0–1


def compute_zone_capacity(zone: Zone, area_per_person: float) -> int:
    rect = zone.rect
    area = (rect.x2 - rect.x1) * (rect.y2 - rect.y1)
    capacity = max(1, int(area / area_per_person))
    return capacity


def compute_zone_metrics(
    layout: Layout,
    positions: np.ndarray,
    risk_cfg: RiskConfig,
    mode: str,
) -> Dict[str, ZoneMetrics]:
    results: Dict[str, ZoneMetrics] = {}

    for z in layout.zones:
        r = z.rect
        mask = (
            (positions[:, 0] >= r.x1)
            & (positions[:, 0] <= r.x2)
            & (positions[:, 1] >= r.y1)
            & (positions[:, 1] <= r.y2)
        )

        # EVAC mode special handling for front zone: ignore evacuees near bottom 25%
        if mode == "EVACUATION" and z.name.lower() == "front":
            cutoff = r.y1 + int((r.y2 - r.y1) * 0.75)
            mask = mask & (positions[:, 1] < cutoff)

        count = int(np.sum(mask))
        capacity = compute_zone_capacity(z, risk_cfg.area_per_person)
        density_ratio = count / capacity if capacity > 0 else 0.0
        density_ratio = min(density_ratio, 1.0)

        results[z.name.lower()] = ZoneMetrics(
            count=count, capacity=capacity, density_ratio=density_ratio
        )

    return results
