import cv2

from ..utils.logger import info


def handle_keyboard() -> bool:
    """
    Only handles quit for now (Q).
    """
    key = cv2.waitKey(30) & 0xFF
    if key == ord("q"):
        info("Operator requested exit")
        return False
    return True
