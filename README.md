# CrowdSynthetic – Concert Crowd Simulation (POC)

CrowdSynthetic is a proof-of-concept simulation for monitoring crowd density and risk in a concert-style layout.  
It uses a configurable layout (zones, stage, exits) and simulates people moving, building risk, and triggering evacuation logic.

This version is a **modularized version of the original POC script**, preserving:

- Layout-driven geometry (`layout.json`)
- Capacity-based zone risks
- Trend-based prediction (“FRONT in X seconds” / “FRONT saturated”)
- AI recommendation text
- Heatmap overlay
- Custom avatar drawing
- EVAC mode logic + POC completion freeze-frame
- CSV + JSON logging of metrics

---

## 🚀 How to Run the Simulation

1. **Install dependencies** (Python 3.9+ recommended):

```bash
pip install -r requirements.txt

python -m src.main

Controls:
Q — Quit simulation
Simulation mode (NORMAL / EVACUATION) is triggered automatically based on crowd risk
Final frame is held after EVAC → NORMAL transition until you press any key
🧠 Notes:
If you get an error like cv2.error, make sure OpenCV is installed correctly.
This is a visual simulation — it opens a real-time window with avatars, heatmap, and UI overlays.
All metrics are logged to concert_risk_log.csv and concert_risk_log.json for analysis.
