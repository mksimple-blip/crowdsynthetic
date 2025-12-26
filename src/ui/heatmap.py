import cv2
import numpy as np


def compute_heatmap(positions: np.ndarray, width: int, height: int):
    """
    Same heatmap logic as your original code.
    """
    heatmap = np.zeros((height, width), dtype=np.float32)
    for x, y in positions:
        ix, iy = int(x), int(y)
        if 0 <= ix < width and 0 <= iy < height:
            heatmap[iy, ix] += 1
    heatmap = cv2.GaussianBlur(heatmap, (0, 0), sigmaX=25, sigmaY=25)
    heatmap_norm = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    heatmap_color = cv2.applyColorMap(heatmap_norm.astype(np.uint8), cv2.COLORMAP_HOT)
    return heatmap_color
