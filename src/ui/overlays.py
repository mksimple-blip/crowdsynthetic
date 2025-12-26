import cv2
import numpy as np

from ..core.layout import Layout
from .avatars import draw_people


def draw_static_elements(frame, layout: Layout, top_ui_height: int, right_margin: int):
    usable_width = layout.width - right_margin - 10
    safe_top = top_ui_height + 20
    safe_bottom = 50

    # Crowd bounding box
    cv2.rectangle(
        frame,
        (20, safe_top),
        (usable_width, layout.height - safe_bottom),
        (200, 200, 200),
        1,
    )

    # Stage
    stage = layout.stage.rect
    cv2.rectangle(
        frame,
        (stage.x1, stage.y1),
        (stage.x2, stage.y2),
        (0, 0, 255),
        2,
    )
    label_x = (stage.x1 + stage.x2) // 2 - 40
    label_y = stage.y1 + 30
    cv2.putText(
        frame,
        "STAGE",
        (label_x, label_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2,
    )

    # Exits
    for ex in layout.exits:
        r = ex.rect
        cv2.rectangle(
            frame,
            (r.x1, r.y1),
            (r.x2, r.y2),
            (0, 150, 0),
            2,
        )
        cv2.putText(
            frame,
            "EXIT",
            (r.x1 + 5, r.y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 150, 0),
            2,
        )

    return frame


def draw_zone_boxes(frame, layout: Layout):
    for z in layout.zones:
        r = z.rect
        cv2.rectangle(frame, (r.x1, r.y1), (r.x2, r.y2), (120, 120, 120), 1)
        cv2.putText(
            frame,
            z.name.upper(),
            (r.x1 + 5, r.y1 + 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (200, 200, 200),
            1,
        )
    return frame


def render_people(frame, positions):
    return draw_people(frame, positions)
