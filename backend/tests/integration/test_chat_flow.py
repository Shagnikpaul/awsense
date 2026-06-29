import json
from unittest.mock import patch

from src.handler import lambda_handler


@patch("src.handler.record_tokens")
@patch("src.handler.record_request")
@patch("src.handler.publish_output_tokens")
@patch("src.handler.generate_answer")
@patch("src.handler.PromptBuilder")
@patch("src.handler.Retriever")
@patch("src.handler.check_request_limit")
@patch("src.handler.load_session")
@patch("src.handler.save_message")
@patch("src.handler.create_conversation")
@patch("src.handler.conversation_exists")
def test_chat_flow(
    mock_conversation_exists,
    mock_create_conversation,
    mock_save_message,
    mock_load_session,
    mock_check_request_limit,
    mock_retriever_cls,
    mock_builder_cls,
    mock_generate_answer,
    mock_publish_metric,
    mock_record_request,
    mock_record_tokens,
):
    mock_load_session.return_value = {}

    mock_check_request_limit.return_value = (
        True,
        None,
    )

    mock_retriever = mock_retriever_cls.return_value

    mock_retriever.search.return_value = [
        {
            "text": "S3 stores objects.",
            "source": {
                "url": "https://docs.aws.amazon.com/s3",
                "title": "S3",
                "topic": "S3",
            },
        }
    ]

    mock_builder = mock_builder_cls.return_value

    mock_builder.build.return_value = "mock prompt"

    mock_generate_answer.return_value = (
        "Amazon S3 is an object storage service.",
        {
            "inputTokens": 10,
            "outputTokens": 20,
        },
    )

    mock_conversation_exists.return_value = True
    mock_save_message.return_value = None

    event = {
        "httpMethod": "POST",
        "path": "/chat",
        "headers": {
            "x-api-key": "test-api-key",
        },
        "body": json.dumps(
            {
                "message": "What is S3?",
                "clientId": "test-client",
                "conversationId": "test-conversation",
            }
        ),
    }

    class MockContext:
        aws_request_id = "test-id"

    with patch("src.handler.API_KEY", "test-api-key"):
        response = lambda_handler(event, MockContext())

    assert response["statusCode"] == 200

    body = json.loads(response["body"])

    assert body["answer"] == "Amazon S3 is an object storage service."
    assert mock_save_message.call_count == 2
