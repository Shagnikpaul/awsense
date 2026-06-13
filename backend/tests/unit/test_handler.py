import json
from unittest.mock import patch
from src.handler import lambda_handler


@patch("src.handler.generate_answer")
@patch("src.handler.Retriever")
@patch("src.handler.PromptBuilder")
def test_chat_success(
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

    event = {
        "httpMethod": "POST",
        "path": "/chat",
        "headers": {"x-api-key": "test-api-key"},
        "body": json.dumps({"message": "What is S3?"}),
    }

    with patch("src.handler.API_KEY", "test-api-key"):
        response = lambda_handler(event, None)

    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert body["answer"] == ("Amazon S3 is an object storage service.")

    assert body["sources"] == ["https://docs.aws.amazon.com/s3"]

    assert body["token_usage"]["inputTokens"] == 100
    assert body["token_usage"]["outputTokens"] == 50
