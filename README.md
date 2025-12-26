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

## How to run

1. Install dependencies:

```bash
pip install -r requirements.txt
