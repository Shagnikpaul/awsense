from src.validator import validate_message
from src.response_formatter import format_response


def lambda_handler(event, context):

    body = event.get("body", {})

    # if body is a string, try to parse it as JSON 
    if isinstance(body, str):
        import json
        body = json.loads(body)

    message = body.get("message", "")

    valid, error = validate_message(message)

    if not valid:
        return {
            "statusCode": 400,
            "body": {
                "error": error
            }
        }

    response = format_response(
        answer=f"Received: {message}",
        sources=[],
        token_usage={
            "inputTokens": 0,
            "outputTokens": 0
        }
    )

    return {
        "statusCode": 200,
        "body": response
    }
