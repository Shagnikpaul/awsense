
from src.prompt_builder import PromptBuilder


def test_prompt_contains_system_prompt():
    builder = PromptBuilder()

    docs = []

    prompt = builder.build("What is S3?", docs)

    assert "You are AWSense" in prompt


def test_prompt_contains_query():
    builder = PromptBuilder()

    docs = [
        {
            "text": "AWS Lambda is a compute service.",
            "source": "doc1.txt",
        }
    ]

    prompt = builder.build("What is Lambda?", docs)

    assert "What is Lambda?" in prompt


def test_prompt_contains_context():
    builder = PromptBuilder()

    docs = [
        {
            "text": "Lambda runs code without servers.",
            "source": "doc1.txt",
        }
    ]

    prompt = builder.build("Explain Lambda", docs)

    assert "Lambda runs code without servers." in prompt


def test_prompt_contains_source():
    builder = PromptBuilder()

    docs = [
        {
            "text": "Serverless compute service",
            "source": "aws.txt",
        }
    ]

    prompt = builder.build("What is AWS?", docs)

    assert "aws.txt" in prompt


def test_prompt_formats_chunks_correctly():
    builder = PromptBuilder()

    docs = [
        {
            "text": "Chunk text",
            "source": "lambda.txt",
        }
    ]

    prompt = builder.build("Explain Lambda", docs)

    assert "[Chunk 1 | Source: lambda.txt]" in prompt
