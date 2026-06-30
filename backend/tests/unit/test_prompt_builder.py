from src.prompt_builder import PromptBuilder


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


def test_prompt_formats_chunks_correctly():
    builder = PromptBuilder()

    docs = [
        {
            "text": "Chunk text",
            "source": "lambda.txt",
        }
    ]

    prompt = builder.build("Explain Lambda", docs)

    assert "[Chunk 1]" in prompt


def test_prompt_contains_context_section():
    builder = PromptBuilder()

    prompt = builder.build("What is EC2?", [])

    assert "CONTEXT:" in prompt


def test_prompt_contains_user_question_section():
    builder = PromptBuilder()

    prompt = builder.build("What is EC2?", [])

    assert "USER QUESTION:" in prompt
