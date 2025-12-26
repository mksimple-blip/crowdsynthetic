import cv2

from ..utils.logger import info


def handle_poc_completion(
    previous_mode: str,
    current_mode: str,
    frame,
    final_display: bool,
    poc_complete_frame_held: bool,
    window_title: str,
):
    """
    Replicates your final POC behavior: when EVAC → NORMAL,
    freeze the last frame and wait for a keypress.
    """
    if (
        previous_mode == "EVACUATION"
        and current_mode == "NORMAL"
        and not poc_complete_frame_held
    ):
        final_display = True
        poc_complete_frame_held = True
        info("POC complete: Evacuation resolved and returned to NORMAL.")
        info("Press any key to close.")
        cv2.imshow(window_title, frame)
        key = cv2.waitKey(30)
        if key != -1:
            return True, final_display, poc_complete_frame_held
    return False, final_display, poc_complete_frame_held
