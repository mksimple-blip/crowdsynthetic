from dataclasses import dataclass
from typing import List, Optional, Tuple

from ..utils.config import PredictionConfig


@dataclass
class PredictionResult:
    text: str
    color: Tuple[int, int, int]
    raw_seconds: Optional[float]


def predict_time_to_threshold(
    history: List[int],
    threshold: int,
    pred_cfg: PredictionConfig,
) -> Optional[float]:
    """
    Same behavior as your predict_time_to_threshold():
    linear trend on last few frames, returns seconds or None.
    """
    if len(history) < 5:
        return None

    recent = history[-10:]
    if len(recent) < 2:
        return None

    deltas = [recent[i + 1] - recent[i] for i in range(len(recent) - 1)]
    if not deltas:
        return None

    avg_delta = sum(deltas) / len(deltas)
    if avg_delta <= 0:
        return None

    current = recent[-1]
    remaining = threshold - current
    if remaining <= 0:
        return 0.0

    frames_needed = remaining / avg_delta
    seconds = frames_needed / pred_cfg.fps
    return round(seconds, 2)


def smooth_prediction(
    prediction_history: List[Optional[float]],
    current_count: int,
    threshold: int,
    pred_cfg: PredictionConfig,
) -> PredictionResult:
    """
    Mirrors your smooth_prediction logic.
    """
    if current_count >= threshold:
        return PredictionResult("FRONT saturated", (0, 0, 255), 0.0)

    if len(prediction_history) < pred_cfg.smooth_window:
        return PredictionResult("Stable", (180, 220, 180), None)

    recent = prediction_history[-pred_cfg.smooth_window:]
    num_active = sum(1 for p in recent if p is not None and p > 0)
    num_saturated = sum(1 for p in recent if p == 0.0)

    if num_saturated >= 3:
        return PredictionResult("FRONT saturated", (0, 0, 255), 0.0)

    if num_active >= 3:
        valid = [p for p in recent if p is not None and p > 0]
        avg_time = sum(valid) / len(valid)
        avg_time = round(avg_time, 1)

        if avg_time <= pred_cfg.short_time_critical:
            color = (0, 0, 255)
        elif avg_time <= pred_cfg.medium_time:
            color = (0, 165, 255)
        else:
            color = (0, 255, 255)

        return PredictionResult(f"FRONT in {avg_time}s", color, avg_time)

    return PredictionResult("Stable", (180, 220, 180), None)
