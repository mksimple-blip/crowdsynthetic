import csv

from ..utils.config import LoggingConfig


class CSVLogger:
    def __init__(self, cfg: LoggingConfig):
        self.cfg = cfg
        with open(self.cfg.csv_filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "frame",
                    "timestamp",
                    "front_density_ratio",
                    "risk_score",
                ]
            )

    def append(
        self,
        frame_count: int,
        timestamp: float,
        front_density_ratio: float,
        risk_score: float,
    ):
        with open(self.cfg.csv_filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    frame_count,
                    f"{timestamp:.3f}",
                    f"{front_density_ratio:.4f}",
                    f"{risk_score:.2f}",
                ]
            )
