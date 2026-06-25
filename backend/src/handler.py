# do no change the order of these imports,
# they are needed to import from the
# python_packages directory
import sys
import time
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
from src.throttle import (  # noqa: E402
    load_session,
    check_request_limit,
    record_request,
    record_tokens,
)  # noqa: E402
from src.logger import log_event, log_error  # noqa: E402
from src.metrics import publish_output_tokens  # noqa: E402
from src.query_classifier import is_greeting  # noqa: E402
from groq import RateLimitError  # noqa: E402

# CORS headers
headers = {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}

API_KEY = os.getenv("API_KEY")


def lambda_handler(event, context):
    start_time = time.time()
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
            "body": json.dumps({"status": "healthy", "service": "AWSense"}),
        }

    # -------------------------
    # METHOD VALIDATION
    # -------------------------
    if path == "/chat" and method != "POST":
        return {
            "statusCode": 405,
            "headers": headers,
            "body": json.dumps({"error": "Method not allowed"}),
        }

    # -------------------------
    # AUTH (ONLY FOR /chat)
    # -------------------------
    if path == "/chat":
        if request_api_key != API_KEY:
            return {
                "statusCode": 401,
                "headers": headers,
                "body": json.dumps({"error": "Unauthorized"}),
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
                "body": json.dumps({"error": "Invalid JSON"}),
            }
    # raise Exception("Alarm test")
    message = body.get("message", "")
    session_id = body.get("sessionId")
    topic_filter = body.get("topicFilter")
    log_event(
        "REQUEST_RECEIVED",
        sessionId=session_id,
        topicFilter=topic_filter,
    )
    if not session_id:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"error": "sessionId is required"}),
        }

    # -------------------------
    # VALIDATION
    # -------------------------
    valid, error = validate_message(message)

    if not valid:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"error": error}),
        }

    session = load_session(session_id)
    allowed, retry_after = check_request_limit(session)

    if not allowed:
        log_event(
            "RATE_LIMITED",
            sessionId=session_id,
            retryAfter=retry_after,
        )
        return {
            "statusCode": 429,
            "headers": {
                **headers,
                "Retry-After": str(retry_after),
            },
            "body": json.dumps(
                {
                    "error": "Rate limit exceeded",
                    "code": "RATE_LIMITED",
                    "requestId": context.aws_request_id,
                }
            ),
        }
    if is_greeting(message):
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(
                {
                    "answer": (
                        "Hello! I'm AWSense. Ask me a question about AWS "
                        "services or architecture and I'll answer using AWS documentation."
                    ),
                    "sources": [],
                    "tokenUsage": {
                        "inputTokens": 0,
                        "outputTokens": 0,
                    },
                }
            ),
        }
    # -------------------------
    # RAG PIPELINE
    # -------------------------
    retriever = Retriever()
    builder = PromptBuilder()
    try:
        docs = retriever.search(message, topic_filter=topic_filter)
        log_event(
            "RETRIEVAL_COMPLETE",
            sessionId=session_id,
            docsReturned=len(docs),
            scores=[round(d.get("score", 0), 4) for d in docs],
        )
        if docs and docs[0].get("is_low_confidence"):
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps(
                    {
                        "answer": (
                            "I don't have knowledge on that topic yet based on my current AWS documentation dataset."
                        ),
                        "sources": [],
                        "tokenUsage": {
                            "inputTokens": 0,
                            "outputTokens": 0,
                        },
                    }
                ),
            }
        prompt = builder.build(message, docs)
        answer, usage = generate_answer(prompt)
        log_event(
            "LLM_USAGE",
            sessionId=session_id,
            inputTokens=usage["inputTokens"],
            outputTokens=usage["outputTokens"],
            totalTokens=usage["inputTokens"] + usage["outputTokens"],
        )
        publish_output_tokens(usage["outputTokens"])

    except RateLimitError:  # specifically for groq...
        log_event(
            "GROQ RATE_LIMITED",
            sessionId=session_id,
        )
        return {
            "statusCode": 429,
            "headers": {
                **headers,
                "Retry-After": str(retry_after),
            },
            "body": json.dumps(
                {
                    "error": "Groq API Rate limit exceeded",
                    "code": "RATE_LIMITED",
                    "requestId": context.aws_request_id,
                }
            ),
        }

    except Exception as e:
        log_error(
            error_type=type(e).__name__,
            error_message=str(e),
            sessionId=session_id,
            topicFilter=topic_filter,
        )
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": "Internal server error"}),
        }

    response = format_response(
        answer=answer,
        sources=list(set([d["source"]["url"] for d in docs])),
        token_usage={
            "inputTokens": usage["inputTokens"],
            "outputTokens": usage["outputTokens"],
        },
    )

    # -------------------------
    # SUCCESS RESPONSE
    # -------------------------
    record_request(session)
    record_tokens(session, usage["outputTokens"])
    duration_ms = int((time.time() - start_time) * 1000)
    log_event(
        "REQUEST_SUCCESS",
        sessionId=session_id,
        topicFilter=topic_filter,
        inputTokens=usage["inputTokens"],
        outputTokens=usage["outputTokens"],
        durationMs=duration_ms,
    )
    return {"statusCode": 200, "headers": headers, "body": json.dumps(response)}
