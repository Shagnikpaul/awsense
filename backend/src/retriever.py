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

headers = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}"
}


class Retriever:
    def __init__(self):
        base_path = Path(__file__).resolve().parents[2]

        self.index = faiss.read_index(
            str(base_path / "vector_store/awsense.index")
        )

        with open(base_path / "vector_store/documents.pkl", "rb") as f:
            data = pickle.load(f)

        self.documents = data["documents"]
        self.sources = data["sources"]

    def get_embedding(self, text: str):

        response = requests.post(
            API_URL,
            headers=headers,
            json={
                "inputs": [text]
            },
            timeout=30
        )

        response.raise_for_status()

        embedding = response.json()

        return np.array(
            embedding,
            dtype=np.float32
        )

    def search(self, query: str, k: int = 3):
        query_vec = self.get_embedding(query)

        distances, indices = self.index.search(query_vec, k)

        results = []

        for i in indices[0]:
            if i < len(self.documents):
                results.append({
                    "text": self.documents[i],
                    "source": self.sources[i]
                })

        return results
