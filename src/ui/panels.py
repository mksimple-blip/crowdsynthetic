import cv2
from textwrap import wrap

from ..utils.config import UIConfig


def draw_panel(frame, x, y, w, h, opacity=0.35):
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y), (x + w, y + h), (40, 40, 40), -1)
    return cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0)


def draw_ui_panels(
    frame,
    ui_cfg: UIConfig,
    width: int,
    height: int,
    risk_score: float,
    risk_color,
    front_density_ratio: float,
    front_count: int,
    front_capacity: int,
    front_risk: float,
    mid_risk: float,
    rear_risk: float,
    ai_message: str,
    mode: str,
    prediction_text: str,
    prediction_color,
    front_threshold: int,
):
    font = cv2.FONT_HERSHEY_SIMPLEX
    line_h = 28
    right_margin = 260

    # TOP BAR
    frame = draw_panel(frame, 0, 0, width, 40, opacity=ui_cfg.panel_opacity)
    cv2.putText(
        frame,
        "Crowd Risk Monitor",
        (20, 27),
        font,
        0.7,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        frame,
        f"{int(risk_score)}%",
        (width // 2 - 40, 27),
        font,
        0.8,
        risk_color,
        2,
    )

    mode_color = {
        "NORMAL": (0, 200, 0),
        "EVACUATION": (0, 0, 255),
    }.get(mode, (255, 255, 255))

    mode_display = f"MODE: {mode}"
    wrapped_mode = wrap(mode_display, width=20)
    for i, line in enumerate(wrapped_mode):
        cv2.putText(
            frame,
            line,
            (width - 180, 27 + i * line_h),
            font,
            0.55,
            mode_color,
            2,
        )

    # RIGHT PANEL
    panel_x = width - right_margin
    panel_y = 60
    panel_w = right_margin - 10
    panel_h = 320

    frame = draw_panel(frame, panel_x, panel_y, panel_w, panel_h, opacity=ui_cfg.panel_opacity)

    text_x = panel_x + 20
    text_y = panel_y + 30

    cv2.putText(frame, "SUMMARY", (text_x, text_y), font, 0.7, ui_cfg.accent_color, 2)
    text_y += 35

    cv2.putText(
        frame,
        f"Front density: {front_density_ratio:.2f}",
        (text_x, text_y),
        font,
        0.55,
        (200, 200, 200),
        1,
    )
    text_y += line_h

    cv2.putText(
        frame,
        f"Front count: {front_count}/{front_capacity}",
        (text_x, text_y),
        font,
        0.55,
        (200, 200, 200),
        1,
    )
    text_y += line_h + 5

    cv2.line(
        frame,
        (panel_x + 10, text_y),
        (panel_x + panel_w - 10, text_y),
        (100, 100, 100),
        1,
    )
    text_y += 20

    cv2.putText(
        frame,
        "Zones (risk)",
        (text_x, text_y),
        font,
        0.55,
        (180, 180, 180),
        1,
    )
    text_y += line_h

    cv2.putText(
        frame,
        f"Front: {front_risk:.2f}",
        (text_x, text_y),
        font,
        0.55,
        (220, 220, 220),
        1,
    )
    text_y += line_h

    cv2.putText(
        frame,
        f"Mid:   {mid_risk:.2f}",
        (text_x, text_y),
        font,
        0.55,
        (220, 220, 220),
        1,
    )
    text_y += line_h

    cv2.putText(
        frame,
        f"Rear:  {rear_risk:.2f}",
        (text_x, text_y),
        font,
        0.55,
        (220, 220, 220),
        1,
    )
    text_y += line_h + 10

    cv2.line(
        frame,
        (panel_x + 10, text_y),
        (panel_x + panel_w - 10, text_y),
        (100, 100, 100),
        1,
    )
    text_y += 20

    cv2.putText(
        frame,
        "PREDICTION",
        (text_x, text_y),
        font,
        0.6,
        ui_cfg.accent_color,
        2,
    )
    text_y += line_h

    cv2.putText(
        frame,
        f"Front cap: {front_capacity}",
        (text_x, text_y),
        font,
        0.52,
        (180, 180, 180),
        1,
    )
    text_y += line_h

    cv2.putText(
        frame,
        f"Threshold: {front_threshold}",
        (text_x, text_y),
        font,
        0.52,
        (180, 180, 180),
        1,
    )
    text_y += line_h

    cv2.putText(
        frame,
        prediction_text,
        (text_x, text_y),
        font,
        0.55,
        prediction_color,
        2,
    )
    text_y += 40

    cv2.line(
        frame,
        (panel_x + 10, text_y),
        (panel_x + panel_w - 10, text_y),
        (100, 100, 100),
        1,
    )
    text_y += 20

    cv2.putText(
        frame,
        "AI RECOMMENDATION",
        (text_x, text_y),
        font,
        0.6,
        ui_cfg.accent_color,
        2,
    )
    text_y += line_h

    wrapped_ai = wrap(ai_message, width=25)
    for line in wrapped_ai:
        cv2.putText(
            frame,
            line,
            (text_x, text_y),
            font,
            0.52,
            (255, 255, 255),
            1,
        )
        text_y += line_h

    # Status bar
    if risk_score < 40:
        alert_message = "Status: Normal crowd conditions"
    elif risk_score < 70:
        alert_message = "WARNING: Growing crowd risk"
    else:
        alert_message = "ALERT: Critical crowd pressure"

    cv2.putText(
        frame,
        alert_message,
        (20, height - 20),
        font,
        0.6,
        (255, 80, 80),
        2,
    )

    return frame
