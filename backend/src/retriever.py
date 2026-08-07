import os
import faiss
import pickle
import numpy as np
import requests
from pathlib import Path
from src.logger import log_event

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

    def search(self, query: str, k: int = 5, topic_filter: str = None):
        query_vec = self.get_embedding(query)

        # retrieve more candidates than needed
        distances, indices = self.index.search(query_vec, k * 10)

        MAX_CHARS_PER_CHUNK = 500

        results = []
        seen_urls = set()

        for distance, i in zip(distances[0], indices[0]):

            if i >= len(self.documents):
                continue

            source = self.sources[i]

            if topic_filter and topic_filter != "All":
                if source.get("topic") != topic_filter:
                    continue

            # deduplicate by source URL
            url = source.get("url")

            if url and url in seen_urls:
                continue

            if url:
                seen_urls.add(url)

            results.append(
                {
                    "text": self.documents[i][:MAX_CHARS_PER_CHUNK],
                    "source": source,
                    "score": float(distance),
                }
            )

            if len(results) == k:
                break
        log_event(
            "TOP_SCORE",
            topScore=results[0]["score"] if results else "NONE",
        )
        if results:
            results[0]["is_low_confidence"] = results[0]["score"] > 1.0

        # fallback
        if not results:
            for i in indices[0][:k]:

                if i >= len(self.documents):
                    continue

                results.append(
                    {
                        "text": self.documents[i][:MAX_CHARS_PER_CHUNK],
                        "source": self.sources[i],
                    }
                )

        return results
