import time


class FPSCounter:
    def __init__(self, smoothing: float = 0.9) -> None:
        self.smoothing = smoothing
        self.last_time = time.time()
        self.fps = 0.0

    def tick(self) -> float:
        now = time.time()
        dt = now - self.last_time
        self.last_time = now
        if dt > 0:
            current_fps = 1.0 / dt
            if self.fps == 0.0:
                self.fps = current_fps
            else:
                self.fps = self.smoothing * self.fps + (1 - self.smoothing) * current_fps
        return self.fps
