from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

DOCS_DIR = Path("../aws_docs_saves/clean")

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []
sources = []

for file in DOCS_DIR.glob("*.txt"):
    text = file.read_text(encoding="utf-8")

    chunks = [text[i:i+500] for i in range(0, len(text), 500)]

    for chunk in chunks:
        documents.append(chunk)
        sources.append(file.name)

print(f"Chunks created: {len(documents)}")

embeddings = model.encode(documents)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

Path("../vector_store").mkdir(exist_ok=True)

faiss.write_index(index, "../vector_store/awsense.index")

with open("../vector_store/documents.pkl", "wb") as f:
    pickle.dump({
        "documents": documents,
        "sources": sources
    }, f)

print("Vector DB created successfully")
