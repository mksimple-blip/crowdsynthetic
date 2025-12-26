def ai_recommendation(front_risk: float, mid_risk: float, rear_risk: float, mode: str) -> str:
    """
    Mirrors your ai_recommendation() text logic.
    """
    if mode == "EVACUATION":
        if front_risk > 0.8:
            return "Front overloaded - evacuation in progress"
        if mid_risk > 0.6:
            return "Mid zone congestion - maintain evacuation flow"
        return "Evacuation active - guide crowd toward exits"

    # NORMAL mode
    if front_risk > 0.65:
        return "Front risk high - prepare intervention"
    if front_risk > 0.5:
        return "Front density rising - monitor closely"
    if mid_risk > 0.9:
        return "Mid zone congestion - monitor movement"
    if rear_risk > 0.7:
        return "Rear zone filling - monitor exit capacity"

    return "Normal operations - no action required"
