from src.handler import lambda_handler
import json
event = {
    "httpMethod": "POST",
    "path": "/chat",
    "body": {
        "message": "What is AWS Route 53?"
    }
}

response = lambda_handler(event, None)

print(json.dumps(response))
