import os
import boto3
import time
from src.logger import log_event

# constraints
MAX_REQUESTS_PER_HOUR = 20
MAX_TOKENS_PER_DAY = 50_000

HOUR_WINDOW_SECONDS = 3600
DAY_WINDOW_SECONDS = 86400


def get_table():
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["THROTTLE_TABLE_NAME"])
    return table


def current_timestamp() -> int:
    return int(time.time())


def get_session_record(session_id: str) -> dict:
    response = get_table().get_item(Key={"sessionId": session_id})

    return response.get("Item", {})


def load_session(session_id: str) -> dict:
    record = get_session_record(session_id)

    if record:
        return record

    now = current_timestamp()

    return {
        "sessionId": session_id,
        "requestCount": 0,
        "tokenCount": 0,
        "windowStart": now,
    }


def save_session(session: dict) -> None:
    get_table().put_item(Item=session)


def record_tokens(session: dict, tokens: int) -> None:
    session["tokenCount"] += tokens
    save_session(session)


def request_window_expired(session: dict) -> bool:
    now = current_timestamp()
    return now - session["windowStart"] >= HOUR_WINDOW_SECONDS


def reset_request_window(session: dict) -> None:
    session["requestCount"] = 0
    session["windowStart"] = current_timestamp()


def check_request_limit(session: dict) -> tuple[bool, int]:
    # reset hourly window if needed
    log_event(
        "THROTTLE_CHECK",
        sessionId=session["sessionId"],
        requestCount=session["requestCount"],
        tokenCount=session["tokenCount"],
        windowStart=session["windowStart"],
        currentTime=current_timestamp(),
    )

    if request_window_expired(session):
        reset_request_window(session)

    # hourly limit check
    if session["requestCount"] >= MAX_REQUESTS_PER_HOUR:
        retry_after = HOUR_WINDOW_SECONDS - (
            current_timestamp() - session["windowStart"]
        )
        log_event(
            "THROTTLE_REJECTED",
            reason="REQUEST_LIMIT",
            sessionId=session["sessionId"],
            requestCount=session["requestCount"],
            retryAfter=retry_after,
        )
        return False, max(retry_after, 0)

    # daily token limit check
    if session["tokenCount"] >= MAX_TOKENS_PER_DAY:
        log_event(
            "THROTTLE_REJECTED",
            reason="TOKEN_LIMIT",
            sessionId=session["sessionId"],
            tokenCount=session["tokenCount"],
        )
        return False, DAY_WINDOW_SECONDS

    return True, 0


def record_request(session: dict) -> None:
    session["requestCount"] += 1
    save_session(session)
