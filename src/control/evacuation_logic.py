from dataclasses import dataclass

from ..ai.zone_risk import ZoneMetrics
from ..utils.config import RiskConfig


@dataclass
class EvacuationState:
    min_evac_duration_frames: int = 60  # 2 seconds at 30 FPS


def update_mode(
    mode: str,
    front_metrics: ZoneMetrics,
    evac_state: EvacuationState,
    evac_timer: int,
    risk_cfg: RiskConfig,
):
    previous_mode = mode

    if mode == "NORMAL":
        if front_metrics.density_ratio > risk_cfg.front_high_threshold:
            mode = "EVACUATION"
            evac_timer = 0

    elif mode == "EVACUATION":
        evac_timer += 1
        if (
            evac_timer > evac_state.min_evac_duration_frames
            and front_metrics.density_ratio < risk_cfg.front_low_threshold
        ):
            mode = "NORMAL"

    return mode, previous_mode, evac_timer
