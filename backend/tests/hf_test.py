import requests
from dotenv import load_dotenv
import os

load_dotenv()
HF_TOKEN = os.getenv('HF_TOKEN')

API_URL = ("https://router.huggingface.co",
           "/hf-inference/models/sentence-transformers/",
           "all-MiniLM-L6-v2/pipeline/feature-extraction")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}


def get_embeddings(texts: list[str]) -> list[list[float]]:
    response = requests.post(API_URL, headers=headers, json={"inputs": texts})
    response.raise_for_status()
    return response.json()  # returns list of 384-dim vectors


# Single text
embedding = get_embeddings(["What is Amazon S3?"])
print(len(embedding[0]))  # 384

# Multiple texts at once
embeddings = get_embeddings([
    "What is Amazon S3?",
    "How does EC2 auto-scaling work?"
])
print(embeddings)  # 2
