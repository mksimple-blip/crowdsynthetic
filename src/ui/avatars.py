import cv2
import numpy as np


def draw_avatar(frame, x: float, y: float, color=(180, 220, 255)):
    """
    Same avatar drawing as your original code.
    """
    x = int(x)
    y = int(y)
    cv2.circle(frame, (x, y - 10), 7, color, -1)
    cv2.line(frame, (x, y - 4), (x, y + 12), color, 4)
    cv2.line(frame, (x, y - 2), (x - 8, y + 8), color, 3)
    cv2.line(frame, (x, y - 2), (x + 8, y + 8), color, 3)
    cv2.line(frame, (x, y + 12), (x - 5, y + 24), color, 3)
    cv2.line(frame, (x, y + 12), (x + 5, y + 24), color, 3)


def draw_people(frame, positions: np.ndarray):
    for x, y in positions:
        draw_avatar(frame, x, y)
    return frame
