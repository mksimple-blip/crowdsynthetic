from typing import Dict, Tuple, List

from .zone_risk import ZoneMetrics


def compute_global_risk(
    front_density_ratio: float, risk_history: List[float]
) -> Tuple[float, Tuple[int, int, int], List[float]]:
    # This mirrors your original compute_global_risk
    raw_risk = front_density_ratio * 100.0
    risk_history.append(raw_risk)
    if len(risk_history) > 15:
        risk_history.pop(0)

    risk_score = sum(risk_history) / len(risk_history)
    risk_color = (0, 255, 0)
    if risk_score > 60:
        risk_color = (0, 0, 255)
    elif risk_score > 30:
        risk_color = (0, 255, 255)
    return risk_score, risk_color, risk_history
