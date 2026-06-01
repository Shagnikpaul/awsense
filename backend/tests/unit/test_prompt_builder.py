from src.prompt_builder import build_prompt


def test_prompt_contains_question():

    prompt = build_prompt(
        ["S3 stores objects"],
        "What is S3?"
    )

    assert "What is S3?" in prompt
