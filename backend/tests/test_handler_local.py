from src.handler import lambda_handler

event = {
    "httpMethod": "POST",
    "path": "/chat",
    "body": {
        "message": "What is AWS Lambda?"
    }
}

response = lambda_handler(event, None)

print(response)