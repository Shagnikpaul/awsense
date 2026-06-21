from src.handler import lambda_handler


def test_health_endpoint():
    event = {
        "httpMethod": "GET",
        "path": "/health",
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 200
