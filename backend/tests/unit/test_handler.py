import json
from unittest.mock import patch
from src.handler import lambda_handler


@patch("src.handler.generate_answer")
@patch("src.handler.Retriever")
@patch("src.handler.PromptBuilder")
@patch("src.handler.record_tokens")
@patch("src.handler.record_request")
@patch("src.handler.check_request_limit")
@patch("src.handler.load_session")
@patch("src.handler.publish_output_tokens")
def test_chat_success(
    mock_publish_output_tokens,
    mock_load_session,
    mock_check_request_limit,
    mock_record_request,
    mock_record_tokens,
    mock_prompt_builder,
    mock_retriever,
    mock_generate_answer,
):
    # Mock retriever search results
    mock_retriever.return_value.search.return_value = [
        {
            "text": "Amazon S3 is object storage",
            "source": {"url": "https://docs.aws.amazon.com/s3"},
        }
    ]

    # Mock prompt builder
    mock_prompt_builder.return_value.build.return_value = "Mocked prompt"

    # Mock LLM response
    mock_generate_answer.return_value = (
        "Amazon S3 is an object storage service.",
        {
            "inputTokens": 100,
            "outputTokens": 50,
        },
    )

    mock_load_session.return_value = {}

    mock_check_request_limit.return_value = (
        True,
        None,
    )

    event = {
        "httpMethod": "POST",
        "path": "/chat",
        "headers": {"x-api-key": "test-api-key"},
        "body": json.dumps({"message": "What is S3?",  "sessionId": "test-session"}),
    }

    with patch("src.handler.API_KEY", "test-api-key"):
        response = lambda_handler(event, None)

    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert body["answer"] == ("Amazon S3 is an object storage service.")

    assert body["sources"] == ["https://docs.aws.amazon.com/s3"]

    assert body["token_usage"]["inputTokens"] == 100
    assert body["token_usage"]["outputTokens"] == 50
