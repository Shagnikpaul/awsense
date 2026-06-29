import json
from unittest.mock import patch

from src.handler import lambda_handler


def test_topic_filter_passed_to_retriever():
    with patch("src.handler.conversation_exists") as mock_conversation_exists, patch(
        "src.handler.create_conversation"
    ) as mock_create_conversation, patch(  # noqa
        "src.handler.save_message"
    ) as mock_save_message, patch(  # noqa
        "src.handler.load_session"
    ) as mock_load_session, patch(
        "src.handler.check_request_limit"
    ) as mock_check_request_limit, patch(
        "src.handler.Retriever"
    ) as mock_retriever_cls, patch(
        "src.handler.PromptBuilder"
    ) as mock_builder_cls, patch(
        "src.handler.generate_answer"
    ) as mock_generate_answer, patch(
        "src.handler.publish_output_tokens"
    ), patch(
        "src.handler.record_request"
    ), patch(
        "src.handler.record_tokens"
    ), patch(
        "src.handler.API_KEY", "test-api-key"
    ):
        mock_load_session.return_value = {}

        mock_check_request_limit.return_value = (
            True,
            None,
        )

        mock_retriever = mock_retriever_cls.return_value

        mock_retriever.search.return_value = [
            {
                "text": "S3 docs",
                "source": {"url": "https://docs.aws.amazon.com/s3"},
            }
        ]

        mock_builder = mock_builder_cls.return_value

        mock_builder.build.return_value = "prompt"

        mock_conversation_exists.return_value = True

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
                    "clientId": "test-client",
                    "conversationId": "test-conversation",
                    "topicFilter": "S3",
                }
            ),
        }

        class MockContext:
            aws_request_id = "test-id"

        with patch("src.handler.API_KEY", "test-api-key"):
            lambda_handler(
                event,
                MockContext(),
            )

        mock_retriever.search.assert_called_once_with(
            "What is S3?",
            topic_filter="S3",
        )
