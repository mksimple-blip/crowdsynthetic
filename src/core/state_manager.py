from dataclasses import dataclass


@dataclass
class SystemState:
    mode: str = "NORMAL"  # NORMAL or EVACUATION
    frame: int = 0
    evac_timer: int = 0
    final_display: bool = False
    poc_complete_frame_held: bool = False
