import os
import faiss
import pickle
import numpy as np
import requests
from pathlib import Path

API_URL = (
    "https://router.huggingface.co/hf-inference/models/"
    "sentence-transformers/all-MiniLM-L6-v2/"
    "pipeline/feature-extraction"
)

headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}


class Retriever:
    def __init__(self):
        base_path = Path(__file__).resolve().parents[1]

        self.index = faiss.read_index(str(base_path / "vector_store/awsense.index"))

        with open(base_path / "vector_store/documents.pkl", "rb") as f:
            data = pickle.load(f)

        self.documents = data["documents"]
        self.sources = data["sources"]

    def get_embedding(self, text: str):

        response = requests.post(
            API_URL, headers=headers, json={"inputs": [text]}, timeout=30
        )

        response.raise_for_status()

        embedding = response.json()

        return np.array(embedding, dtype=np.float32)

    def search(self, query: str, k: int = 3, topic_filter: str = None):
        if topic_filter and topic_filter != "All":
            query = f"AWS Service: {topic_filter}\nUser Question: {query}"

        query_vec = self.get_embedding(query)

        distances, indices = self.index.search(query_vec, k * 10)

        results = []

        for i in indices[0]:

            if i >= len(self.documents):
                continue

            source = self.sources[i]

            if topic_filter and topic_filter != "All":
                if source.get("topic") != topic_filter:
                    continue

            results.append({"text": self.documents[i], "source": source})

            if len(results) == k:
                break

        # fallback (IMPORTANT)
        if not results:
            for i in indices[0][:k]:
                if i < len(self.documents):
                    results.append(
                        {"text": self.documents[i], "source": self.sources[i]}
                    )

        return results
