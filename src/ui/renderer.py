import cv2
import numpy as np

from ..core.layout import Layout
from ..utils.config import UIConfig, SimulationConfig
from .heatmap import compute_heatmap
from .overlays import draw_static_elements, draw_zone_boxes, render_people
from .panels import draw_ui_panels


class Renderer:
    def __init__(self, layout: Layout, ui_cfg: UIConfig, sim_cfg: SimulationConfig):
        self.layout = layout
        self.ui_cfg = ui_cfg
        self.sim_cfg = sim_cfg

    def render(
        self,
        frame,
        positions,
        risk_score,
        risk_color,
        front_density_ratio,
        front_count,
        front_capacity,
        front_risk,
        mid_risk,
        rear_risk,
        ai_message,
        mode,
        prediction_text,
        prediction_color,
        front_threshold,
    ):
        cv2.imshow(self.ui_cfg.window_title, frame)

    def build_frame(
        self,
        positions,
        risk_score,
        risk_color,
        front_density_ratio,
        front_count,
        front_capacity,
        front_risk,
        mid_risk,
        rear_risk,
        ai_message,
        mode,
        prediction_text,
        prediction_color,
        front_threshold,
    ):
        # Background
        frame = np.full(
            (self.layout.height, self.layout.width, 3),
            self.ui_cfg.bg_color,
            dtype=np.uint8,
        )

        # Static elements
        frame = draw_static_elements(
            frame,
            self.layout,
            self.sim_cfg.top_ui_height,
            self.sim_cfg.right_margin,
        )

        # People
        frame = render_people(frame, positions)

        # Heatmap overlay
        heatmap = compute_heatmap(
            positions,
            self.layout.width,
            self.layout.height,
        )
        frame = cv2.addWeighted(frame, 0.85, heatmap, 0.15, 0)

        # Zone boxes
        frame = draw_zone_boxes(frame, self.layout)

        # UI panels
        frame = draw_ui_panels(
            frame,
            self.ui_cfg,
            self.layout.width,
            self.layout.height,
            risk_score,
            risk_color,
            front_density_ratio,
            front_count,
            front_capacity,
            front_risk,
            mid_risk,
            rear_risk,
            ai_message,
            mode,
            prediction_text,
            prediction_color,
            front_threshold,
        )

        return frame

    def show_frame(self, frame):
        cv2.imshow(self.ui_cfg.window_title, frame)
