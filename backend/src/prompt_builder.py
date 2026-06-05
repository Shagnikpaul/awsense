class PromptBuilder:
    def __init__(self):
        self.system_prompt = (
            "You are AWSense, an AWS documentation assistant. "
            "You MUST answer ONLY using the provided context. "
            "If the answer is not in the context, say you don't know."
        )

    def build(self, query: str, retrieved_docs: list) -> str:
        context_blocks = []

        for i, doc in enumerate(retrieved_docs):
            context_blocks.append(
                f"[Chunk {i+1} | Source: {doc['source']}]\n{doc['text']}"
            )

        context = "\n\n".join(context_blocks)

        prompt = f"""
SYSTEM:
{self.system_prompt}

CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER:
"""

        return prompt.strip()
