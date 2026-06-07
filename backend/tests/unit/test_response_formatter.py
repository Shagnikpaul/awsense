from src.response_formatter import format_response


def test_format_response_structure():
    response = format_response(
        answer="AWS Lambda is serverless compute.",
        sources=["doc1.txt", "doc2.txt"],
        token_usage={"inputTokens": 10, "outputTokens": 20}
    )

    assert "answer" in response
    assert "sources" in response
    assert "token_usage" in response


def test_format_response_values():
    response = format_response(
        answer="hello",
        sources=["a.txt"],
        token_usage={"inputTokens": 1, "outputTokens": 2}
    )

    assert response["answer"] == "hello"
    assert response["sources"] == ["a.txt"]
    assert response["token_usage"]["inputTokens"] == 1
