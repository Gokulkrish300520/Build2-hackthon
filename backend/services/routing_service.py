seen_events = set()


def should_process_event(event_id: int) -> bool:
    """
    Prevent duplicate processing
    """
    if event_id in seen_events:
        return False

    seen_events.add(event_id)
    return True


def decrement_ttl(event: dict) -> dict:
    """
    Decrease TTL safely
    """
    ttl = event.get("ttl", 0)

    if ttl <= 0:
        return None

    event["ttl"] = ttl - 1
    return event


def prioritize_event(event: dict) -> int:
    """
    Higher number = higher priority
    """

    risk_level = event.get("risk_level", 1)

    if risk_level == 4:
        return 1  # Highest priority
    if risk_level == 3:
        return 2
    if risk_level == 2:
        return 3
    return 4  # Lowest