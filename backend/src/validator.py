def validate_message(message: str) -> tuple[bool, str]:
    """
    Returns:
    (True, "") if valid
    (False, reason) if invalid
    """

    if not message:
        return False, "Message cannot be empty"
    
    if len(message.strip()) == 0:
        return False, "Message cannot be empty"
    
    # 500 character limit for messages
    if len(message) > 500:
        return False, "Message exceeds 500 character limit"

    return True, ""
