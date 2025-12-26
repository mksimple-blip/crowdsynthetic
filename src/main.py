import time

import cv2

from .core.layout import Layout
from .core.simulation_engine import SimulationEngine
from .core.state_manager import SystemState
from .ai.zone_risk import compute_zone_metrics
from .ai.risk_model import compute_global_risk
from .ai.prediction_engine import predict_time_to_threshold, smooth_prediction
from .ai.recommendation_engine import ai_recommendation
from .control.evacuation_logic import EvacuationState, update_mode
from .control.hitl_controller import handle_keyboard
from .control.poc_completion import handle_poc_completion
from .logging.csv_logger import CSVLogger
from .logging.json_logger import JSONLogger
from .ui.renderer import Renderer
from .utils.config import Config
from .utils.logger import info
from .utils.timers import FPSCounter


def main():
    cfg = Config()
    layout = Layout()
    sim = SimulationEngine(layout, cfg.sim)
    state = SystemState()
    evac_state = EvacuationState()
    renderer = Renderer(layout, cfg.ui, cfg.sim)
    csv_logger = CSVLogger(cfg.log)
    json_logger = JSONLogger(cfg.log)
    fps_counter = FPSCounter()

    risk_history = []
    front_history = []
    prediction_history = []

    start_time = time.time()

    info("Starting CrowdSynthetic concert POC")

    running = True
    last_frame = None

    while running:
        # Simulation step
        snapshot = sim.step(state.mode)
        positions = snapshot.positions

        # Zone metrics
        zone_metrics = compute_zone_metrics(
            layout,
            positions,
            cfg.risk,
            state.mode,
        )
        # Ensure names
        front_m = zone_metrics.get("front")
        mid_m = zone_metrics.get("mid")
        rear_m = zone_metrics.get("rear")

        front_density_ratio = front_m.density_ratio if front_m else 0.0

        # Global risk
        risk_score, risk_color, risk_history = compute_global_risk(
            front_density_ratio,
            risk_history,
        )

        # FRONT history & prediction
        front_count = front_m.count if front_m else 0
        front_capacity = front_m.capacity if front_m else 1
        front_threshold = int(front_capacity * 0.8)

        front_history.append(front_count)
        front_pred_seconds = predict_time_to_threshold(
            front_history,
            front_threshold,
            cfg.pred,
        )

        prediction_history.append(front_pred_seconds)
        if len(prediction_history) > cfg.pred.history_window:
            prediction_history.pop(0)

        pred_result = smooth_prediction(
            prediction_history,
            front_count,
            front_threshold,
            cfg.pred,
        )

        # EVAC logic
        state.mode, previous_mode, state.evac_timer = update_mode(
            state.mode,
            front_m,
            evac_state,
            state.evac_timer,
            cfg.risk,
        )

        # AI recommendation
        front_risk = front_m.density_ratio if front_m else 0.0
        mid_risk = mid_m.density_ratio if mid_m else 0.0
        rear_risk = rear_m.density_ratio if rear_m else 0.0

        ai_message = ai_recommendation(
            front_risk,
            mid_risk,
            rear_risk,
            state.mode,
        )

        # Build frame
        frame = renderer.build_frame(
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
            state.mode,
            pred_result.text,
            pred_result.color,
            front_threshold,
        )

        state.frame = snapshot.frame
        last_frame = frame.copy()

        # POC completion handling (EVAC → NORMAL freeze)
        should_break, state.final_display, state.poc_complete_frame_held = handle_poc_completion(
            previous_mode,
            state.mode,
            last_frame,
            state.final_display,
            state.poc_complete_frame_held,
            cfg.ui.window_title,
        )
        if should_break:
            break

        # Logging
        timestamp = time.time() - start_time
        zone_counts_simple = {k: v.count for k, v in zone_metrics.items()}
        zone_risks_simple = {k: v.density_ratio for k, v in zone_metrics.items()}

        csv_logger.append(
            snapshot.frame,
            timestamp,
            front_density_ratio,
            risk_score,
        )

        json_logger.append(
            snapshot.frame,
            timestamp,
            front_density_ratio,
            risk_score,
            zone_counts_simple,
            zone_risks_simple,
            front_history,
            [p if p is not None else -1 for p in prediction_history],
        )

        # FPS
        fps = fps_counter.tick()
        # (You can overlay FPS in UI later if you want.)

        # Display
        renderer.show_frame(frame)

        # Keyboard
        running = handle_keyboard()
        if not running:
            break

        if cv2.getWindowProperty(cfg.ui.window_title, cv2.WND_PROP_VISIBLE) < 1:
            info("Window closed by user")
            break

    # Final JSON write
    json_logger.write()
    cv2.destroyAllWindows()
    info("Simulation ended")


if __name__ == "__main__":
    main()
