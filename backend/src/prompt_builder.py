class PromptBuilder:

    def build(self, query: str, retrieved_docs: list) -> str:

        context_blocks = []

        for i, doc in enumerate(retrieved_docs):
            # context_blocks.append(
            #     f"[Chunk {i+1} | Source: {doc['source']}]\n{doc['text']}"
            # )
            # no need of urls in context for now...
            context_blocks.append(
                f"[Chunk {i+1}]\n{doc['text']}"
            )

        context = "\n\n".join(context_blocks)

        prompt = f"""
CONTEXT:
{context}

USER QUESTION:
{query}
"""

        return prompt.strip()
