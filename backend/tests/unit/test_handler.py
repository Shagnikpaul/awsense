from src.handler import lambda_handler


def test_valid_request():

    event = {
        "body": {
            "message": "What is S3?"
        }
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 200


def test_invalid_request():

    event = {
        "body": {
            "message": ""
        }
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 400
