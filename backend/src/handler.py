from src.validator import validate_message
from src.response_formatter import format_response
from src.retriever import Retriever
from src.prompt_builder import PromptBuilder
from src.llm_chat import generate_answer

import json

# CORS headers
headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
}


def lambda_handler(event, context):
    method = event.get("httpMethod")
    path = event.get("path", "")

    if method == "GET" and path == "/health":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "status": "healthy",
                "service": "AWSense"
            })
        }

    if method != "POST" and path != "/health":
        return {
            "statusCode": 405,
            "headers": headers,
            "body": json.dumps({"error": "Method not allowed"})
        }

    body = event.get("body") or "{}"

    # if body is a string, try to parse it as JSON
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except Exception:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "Invalid JSON"
                }),
                "headers": headers
            }

    message = body.get("message", "")

    valid, error = validate_message(message)

    if not valid:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": error
            }),
            "headers": headers
        }

    retriever = Retriever()
    builder = PromptBuilder()

    docs = retriever.search(message)
    prompt = builder.build(message, docs)

    # answer = docs[0]["text"] if docs else "No relevant context found."
    answer, usage = generate_answer(prompt)

    response = format_response(
        answer=answer,
        sources=list(set([d["source"] for d in docs])),
        token_usage={
            "inputTokens": usage["inputTokens"],
            "outputTokens": usage["outputTokens"]
        }
    )

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps(response)
    }
