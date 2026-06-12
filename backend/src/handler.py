# do no change the order of these imports,
# they are needed to import from the
# python_packages directory
import sys
import json
import os
from pathlib import Path
current_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(current_dir / "python_packages"))
from src.llm_chat import generate_answer  # noqa: E402
from src.prompt_builder import PromptBuilder  # noqa: E402
from src.retriever import Retriever  # noqa: E402
from src.response_formatter import format_response  # noqa: E402
from src.validator import validate_message  # noqa: E402

# CORS headers
headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
}

API_KEY = os.getenv("API_KEY")


def lambda_handler(event, context):
    method = event.get("httpMethod")
    path = event.get("path", "")

    request_headers = event.get("headers") or {}
    request_api_key = request_headers.get("x-api-key")

    # -------------------------
    # PUBLIC ENDPOINT: HEALTH
    # -------------------------
    if method == "GET" and path == "/health":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "status": "healthy",
                "service": "AWSense"
            })
        }

    # -------------------------
    # METHOD VALIDATION
    # -------------------------
    if path == "/chat" and method != "POST":
        return {
            "statusCode": 405,
            "headers": headers,
            "body": json.dumps({
                "error": "Method not allowed"
            })
        }

    # -------------------------
    # AUTH (ONLY FOR /chat)
    # -------------------------
    if path == "/chat":
        if request_api_key != API_KEY:
            return {
                "statusCode": 401,
                "headers": headers,
                "body": json.dumps({
                    "error": "Unauthorized"
                })
            }

    # -------------------------
    # PARSE BODY
    # -------------------------
    body = event.get("body") or "{}"

    if isinstance(body, str):
        try:
            body = json.loads(body)
        except Exception:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({
                    "error": "Invalid JSON"
                })
            }

    message = body.get("message", "")

    # -------------------------
    # VALIDATION
    # -------------------------
    valid, error = validate_message(message)

    if not valid:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({
                "error": error
            })
        }

    # -------------------------
    # RAG PIPELINE
    # -------------------------
    retriever = Retriever()
    builder = PromptBuilder()

    docs = retriever.search(message)
    prompt = builder.build(message, docs)

    answer, usage = generate_answer(prompt)

    response = format_response(
        answer=answer,
        sources=list(set([d["source"]["url"] for d in docs])),
        token_usage={
            "inputTokens": usage["inputTokens"],
            "outputTokens": usage["outputTokens"]
        }
    )

    # -------------------------
    # SUCCESS RESPONSE
    # -------------------------
    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps(response)
    }
