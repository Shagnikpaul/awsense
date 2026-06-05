from src.handler import lambda_handler


def test_lambda_handler_success():
    event = {
        "httpMethod": "POST",
        "path": "/chat",
        "body": {
            "message": "What is AWS Lambda?"
        }
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 200
    assert "body" in response


def test_lambda_handler_invalid_method():
    event = {
        "httpMethod": "GET",
        "path": "/chat",
        "body": {}
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 405


def test_lambda_handler_empty_message():
    event = {
        "httpMethod": "POST",
        "path": "/chat",
        "body": {
            "message": ""
        }
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 400
