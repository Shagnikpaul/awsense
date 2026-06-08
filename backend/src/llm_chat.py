from groq import Groq
import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(prompt: str) -> tuple[str | None, dict]:

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are AWSense, an AWS documentation assistant. "
                    "Answer ONLY from the provided context."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2,
        max_tokens=512
    )

    answer = response.choices[0].message.content

    usage = {
        "inputTokens": response.usage.prompt_tokens,  # type: ignore
        "outputTokens": response.usage.completion_tokens  # type: ignore
    }
    return answer, usage
