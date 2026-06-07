def format_response(answer, sources, token_usage):
    return {
        "answer": answer,
        "sources": sources,
        "token_usage": token_usage
    }
