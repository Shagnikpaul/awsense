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
def test_topic_filter_passed_to_retriever(
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

    mock_retriever.search.return_value = []

    mock_builder = mock_builder_cls.return_value

    mock_builder.build.return_value = "prompt"

    mock_generate_answer.return_value = (
        "answer",
        {
            "inputTokens": 1,
            "outputTokens": 1,
        },
    )

    event = {
        "httpMethod": "POST",
        "path": "/chat",
        "headers": {
            "x-api-key": "test-api-key",
        },
        "body": json.dumps(
            {
                "message": "What is S3?",
                "sessionId": "test-session",
                "topicFilter": "S3",
            }
        ),
    }

    class MockContext:
        aws_request_id = "test-id"

    lambda_handler(
        event,
        MockContext(),
    )

    mock_retriever.search.assert_called_once_with(
        "What is S3?",
        topic_filter="S3",
    )
