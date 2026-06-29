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
from src.chat_history import (  # noqa: E402
    create_conversation,
    save_message,
    get_conversation,
    list_conversations,
    conversation_exists,
    get_conversation_metadata,
)

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
    # GET CONVERSATIONS (all messsages in a conversation)
    # -------------------------
    if method == "GET" and path == "/conversations":

        if request_api_key != API_KEY:
            return {
                "statusCode": 401,
                "headers": headers,
                "body": json.dumps({"error": "Unauthorized"}),
            }

        client_id = request_headers.get("x-client-id")

        if not client_id:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"error": "clientId header is required"}),
            }

        conversations = list_conversations(client_id)

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(conversations),
        }
    # -------------------------
    # GET CONVERSATION
    # -------------------------
    if method == "GET" and path.startswith("/conversations/"):

        if request_api_key != API_KEY:
            return {
                "statusCode": 401,
                "headers": headers,
                "body": json.dumps({"error": "Unauthorized"}),
            }
        # first check if the conversation actually belongs to the cliend requesting it...
        conversation_id = path.split("/")[-1]
        client_id = request_headers.get("x-client-id")
        if not client_id:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"error": "clientId header is required"}),
            }
        conversation = get_conversation_metadata(conversation_id)
        if conversation is None:
            return {
                "statusCode": 404,
                "headers": headers,
                "body": json.dumps({"error": "Conversation not found"}),
            }

        if conversation["clientId"] != client_id:
            return {
                "statusCode": 403,
                "headers": headers,
                "body": json.dumps({"error": "Forbidden"}),
            }
        messages = get_conversation(conversation_id)

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(messages),
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
    client_id = body.get("clientId")
    conversation_id = body.get("conversationId")
    topic_filter = body.get("topicFilter")
    log_event(
        "REQUEST_RECEIVED",
        sessionId=client_id,
        topicFilter=topic_filter,
    )
    if not client_id:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"error": "clientId is required"}),
        }

    if not conversation_id:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"error": "conversationId is required"}),
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

    session = load_session(client_id)
    allowed, retry_after = check_request_limit(session)

    if not allowed:
        log_event(
            "RATE_LIMITED",
            sessionId=client_id,
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

    if not conversation_exists(conversation_id):
        create_conversation(
            client_id=client_id,
            conversation_id=conversation_id,
            title=message[:60],
        )

    save_message(
        conversation_id=conversation_id,
        role="user",
        content=message,
    )

    if is_greeting(message):
        greeting_response = {
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

        save_message(
            conversation_id=conversation_id,
            role="assistant",
            content=greeting_response["answer"],
            sources=[],
            token_usage=greeting_response["tokenUsage"],
        )

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(greeting_response),
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
            sessionId=client_id,
            docsReturned=len(docs),
            scores=[round(d.get("score", 0), 4) for d in docs],
        )
        if docs and docs[0].get("is_low_confidence"):
            low_confidence_response = {
                "answer": (
                    "I don't have knowledge on that topic yet based on my current AWS documentation dataset."
                ),
                "sources": [],
                "tokenUsage": {
                    "inputTokens": 0,
                    "outputTokens": 0,
                },
            }

            save_message(
                conversation_id=conversation_id,
                role="assistant",
                content=low_confidence_response["answer"],
                sources=[],
                token_usage=low_confidence_response["tokenUsage"],
            )

            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps(low_confidence_response),
            }
        prompt = builder.build(message, docs)
        answer, usage = generate_answer(prompt)
        log_event(
            "LLM_USAGE",
            sessionId=client_id,
            inputTokens=usage["inputTokens"],
            outputTokens=usage["outputTokens"],
            totalTokens=usage["inputTokens"] + usage["outputTokens"],
        )
        publish_output_tokens(usage["outputTokens"])

    except RateLimitError:  # specifically for groq...
        log_event(
            "GROQ RATE_LIMITED",
            sessionId=client_id,
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
            sessionId=client_id,
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

    save_message(
        conversation_id=conversation_id,
        role="assistant",
        content=response["answer"],
        sources=response["sources"],
        token_usage=response["token_usage"],
    )

    # -------------------------
    # SUCCESS RESPONSE
    # -------------------------
    record_request(session)
    record_tokens(session, usage["outputTokens"])
    duration_ms = int((time.time() - start_time) * 1000)
    log_event(
        "REQUEST_SUCCESS",
        sessionId=client_id,
        topicFilter=topic_filter,
        inputTokens=usage["inputTokens"],
        outputTokens=usage["outputTokens"],
        durationMs=duration_ms,
    )
    return {"statusCode": 200, "headers": headers, "body": json.dumps(response)}
