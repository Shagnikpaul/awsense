import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

# Load ONCE globally (important)
_model = SentenceTransformer("all-MiniLM-L6-v2")


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

        self.model = _model  # reuse global model

    def search(self, query: str, k: int = 3):
        query_vec = self.model.encode(
            [query], convert_to_numpy=True
        ).astype(np.float32)

        distances, indices = self.index.search(query_vec, k)

        results = []

        for i in indices[0]:
            if i < len(self.documents):
                results.append({
                    "text": self.documents[i],
                    "source": self.sources[i]
                })

        return results
