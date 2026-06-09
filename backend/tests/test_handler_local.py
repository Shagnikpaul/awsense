from src.handler import lambda_handler
import json
event = {
    "httpMethod": "POST",
    "path": "/chat",
    "body": {
        "message": "What is Amazon VPC?"
    }
}

response = lambda_handler(event, None)

print(json.dumps(response))
