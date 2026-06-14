from groq import Groq
import os


def generate_answer(prompt: str) -> tuple[str | None, dict]:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """
You are AWSense, an AWS documentation assistant.

Rules:
- Answer ONLY from the provided AWS documentation context.
- Do not invent information.
- If the answer is not present in the context or the question is unrelated to AWS, say:
  "I don't have knowledge on that topic yet based on my current AWS documentation dataset."

Format responses in Markdown.
Keep explanations concise and technical.

Follow-up Suggestions:
- At the end of every answer, include:

## Suggested Follow-up Questions
- Question 1
- Question 2

The follow-up questions should be relevant to the user's current AWS topic.
""",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=512,
    )

    answer = response.choices[0].message.content

    usage = {
        "inputTokens": response.usage.prompt_tokens,  # type: ignore
        "outputTokens": response.usage.completion_tokens,  # type: ignore
    }
    return answer, usage
