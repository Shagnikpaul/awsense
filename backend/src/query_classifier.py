GREETINGS = {
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening",
    "thanks",
    "thank you",
    "bye",
}


def is_greeting(message: str) -> bool:
    return message.strip().lower() in GREETINGS