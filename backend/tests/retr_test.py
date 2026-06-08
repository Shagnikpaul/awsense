from src.retriever import Retriever

r = Retriever()
results = r.search("What is AWS Lambda?")

for i, result in enumerate(results, start=1):
    print(f"Result {i}")
    print("Source:", result["source"])
    print("Text:")
    print(result["text"][:500])
    print("-" * 80)
