import dataclasses


@dataclasses.dataclass
class SimulationConfig:
    width: int = 800
    height: int = 600
    num_people: int = 100  # CHANGE CROWD SIZE HERE
    dt: float = 1.0

    # UI margins similar to original script
    right_margin: int = 260
    top_ui_height: int = 40


@dataclasses.dataclass
class RiskConfig:
    area_per_person: float = 900.0  # same flavor as original
    # thresholds expressed as density ratio of capacity
    front_high_threshold: float = 0.8
    front_low_threshold: float = 0.4


@dataclasses.dataclass
class PredictionConfig:
    fps: int = 30
    history_window: int = 10
    smooth_window: int = 5
    short_time_critical: float = 3.0
    medium_time: float = 7.0


@dataclasses.dataclass
class UIConfig:
    window_title: str = "Concert Crowd Simulation"
    font_scale: float = 0.55
    font_thickness: int = 1
    panel_opacity: float = 0.35
    accent_color: tuple[int, int, int] = (0, 180, 255)  # BGR
    bg_color: tuple[int, int, int] = (22, 25, 30)


@dataclasses.dataclass
class LoggingConfig:
    csv_filename: str = "concert_risk_log.csv"
    json_filename: str = "concert_risk_log.json"


@dataclasses.dataclass
class Config:
    sim: SimulationConfig = SimulationConfig()
    risk: RiskConfig = RiskConfig()
    pred: PredictionConfig = PredictionConfig()
    ui: UIConfig = UIConfig()
    log: LoggingConfig = LoggingConfig()
