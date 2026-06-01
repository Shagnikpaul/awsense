def format_response(answer, sources, token_usage):
    return {
        "answer": answer,
        "sources": sources,
        "tokenUsage": token_usage
    }
