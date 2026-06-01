def build_prompt(context_chunks, question):

    context = "\n\n".join(context_chunks)

    return f"""
You are AWSense, an AWS documentation assistant.

Context:
{context}

Question:
{question}

Answer using only the provided context.
"""
