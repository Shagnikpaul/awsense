import json
from unittest.mock import patch

from src.handler import lambda_handler


@patch("src.handler.check_request_limit")
@patch("src.handler.load_session")
def test_rate_limited(
    mock_load_session,
    mock_check_request_limit,
):
    mock_load_session.return_value = {
        "sessionId": "test-session"
    }

    mock_check_request_limit.return_value = (
        False,
        3600,
    )

    event = {
        "httpMethod": "POST",
        "path": "/chat",
        "headers": {
            "x-api-key": "test-api-key"
        },
        "body": json.dumps(
            {
                "message": "What is S3?",
                "sessionId": "test-session",
            }
        ),
    }

    class MockContext:
        aws_request_id = "test-request-id"

    response = lambda_handler(
        event,
        MockContext(),
    )

    assert response["statusCode"] == 429

    assert (
        response["headers"]["Retry-After"]
        == "3600"
    )

    body = json.loads(
        response["body"]
    )

    assert body["code"] == "RATE_LIMITED"
