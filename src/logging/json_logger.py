import json
from typing import Dict, Any, List

from ..utils.config import LoggingConfig


class JSONLogger:
    def __init__(self, cfg: LoggingConfig):
        self.cfg = cfg
        self.metrics: Dict[str, List[Any]] = {
            "frames": [],
            "timestamps": [],
            "front_density_ratio": [],
            "risk_score": [],
            "zone_counts": [],
            "zone_risks": [],
            "front_history": [],
            "prediction_history": [],
        }

    def append(
        self,
        frame_count: int,
        timestamp: float,
        front_density_ratio: float,
        risk_score: float,
        zone_results: Dict[str, int],
        zone_risks: Dict[str, float],
        front_history: List[int],
        prediction_history: List[float],
    ):
        self.metrics["frames"].append(frame_count)
        self.metrics["timestamps"].append(timestamp)
        self.metrics["front_density_ratio"].append(float(front_density_ratio))
        self.metrics["risk_score"].append(float(risk_score))
        self.metrics["zone_counts"].append(zone_results)
        self.metrics["zone_risks"].append(zone_risks)
        self.metrics["front_history"].append(list(front_history))
        self.metrics["prediction_history"].append(list(prediction_history))

    def write(self):
        with open(self.cfg.json_filename, "w") as f:
            json.dump(self.metrics, f, indent=2)
