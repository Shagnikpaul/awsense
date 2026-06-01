from src.response_formatter import format_response


def test_format_response():

    response = format_response(
        "answer",
        [],
        {"inputTokens": 10, "outputTokens": 20}
    )

    assert response["answer"] == "answer"
