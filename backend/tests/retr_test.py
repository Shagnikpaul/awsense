from src.retriever import Retriever
import requests

r = Retriever()
results = r.search("What is AWS Route 53?")

for i, result in enumerate(results, start=1):
    print(f"Result {i}")
    print("Source:", result["source"])
    print("Text:")
    print(result["text"][:500])
    print("-" * 80)

# print(requests.get("https://huggingface.co").status_code)