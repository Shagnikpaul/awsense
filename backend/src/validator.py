def validate_message(message: str) -> tuple[bool, str]:
    """
    Returns:
    (True, "") if valid
    (False, reason) if invalid
    """

    blocked_patterns = [
        "ignore previous instructions",
        "reveal system prompt",
        "show hidden prompt",
        "act as root",
        "jailbreak",
    ]

    if not message or not message.strip():
        return False, "Message cannot be empty"

    message = message.strip()

    if len(message) > 500:
        return False, "Message exceeds 500 character limit"

    lower = message.lower()

    for pattern in blocked_patterns:
        if pattern in lower:
            return False, f"Message contains blocked pattern: {pattern}"

    return True, ""
