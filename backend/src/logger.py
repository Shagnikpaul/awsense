import json
import logging
import os
from decimal import Decimal

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)


def json_serializer(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


def log_event(event_type: str, **kwargs):
    logger.info(
        json.dumps(
            {
                "eventType": event_type,
                **kwargs,
            },
            default=json_serializer,
        )
    )


def log_error(error_type: str, error_message: str, **kwargs):
    logger.error(
        json.dumps(
            {
                "eventType": "ERROR",
                "errorType": error_type,
                "errorMessage": error_message,
                **kwargs,
            },
            default=json_serializer,
        )
    )
