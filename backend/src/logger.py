import json
import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)


def log_event(event_type: str, **kwargs):
    logger.info(
        json.dumps(
            {
                "eventType": event_type,
                **kwargs,
            }
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
            }
        )
    )