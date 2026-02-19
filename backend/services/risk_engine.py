def calculate_risk(event_type: int) -> int:
    """
    event_type:
    1 = Elephant
    2 = Human
    3 = Weapon
    4 = Elephant + Human
    5 = Human + Weapon
    """

    if event_type == 4:
        return 4  # Critical
    if event_type == 5:
        return 4  # Critical
    if event_type == 2:
        return 3  # High
    if event_type == 1:
        return 2  # Medium
    return 1  # Low


def calculate_radius(risk_level: int) -> int:
    """
    Returns radius in meters
    """

    if risk_level == 4:
        return 600
    if risk_level == 3:
        return 400
    if risk_level == 2:
        return 500
    return 300


def process_event(event: dict) -> dict:
    """
    Recalculate risk + radius before forwarding.
    """

    event_type = event.get("event_type", 1)

    risk_level = calculate_risk(event_type)
    radius = calculate_radius(risk_level)

    event["risk_level"] = risk_level
    event["radius_m"] = radius

    return event