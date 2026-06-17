from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import pickle
import json
from pathlib import Path

# -------------------------
# PATHS
# -------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = BASE_DIR / "aws_docs_saves/clean"

METADATA_FILE = BASE_DIR / "aws_docs_saves/metadata.json"

VECTOR_STORE_DIR = BASE_DIR / "backend" / "vector_store"

# -------------------------
# LOAD METADATA
# -------------------------

with open(METADATA_FILE, "r", encoding="utf-8") as f:
    metadata = json.load(f)

# -------------------------
# LOAD EMBEDDING MODEL
# -------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------------
# STORAGE
# -------------------------

documents = []
sources = []

# -------------------------
# PROCESS DOCUMENTS
# -------------------------

for file in DOCS_DIR.glob("*.txt"):

    text = file.read_text(encoding="utf-8")

    # Simple chunking
    chunks = [text[i: i + 500] for i in range(0, len(text), 500)]

    for chunk in chunks:

        documents.append(chunk)

        meta = metadata.get(file.name, {})

        sources.append(
            {
                "file": file.name,
                "title": meta.get("title", "Untitled"),
                "url": meta.get("url", ""),
                "topic": meta.get("topic", "Unknown")
            }
        )

print(f"Chunks created: {len(documents)}")

# -------------------------
# CREATE EMBEDDINGS
# -------------------------

embeddings = model.encode(documents, convert_to_numpy=True).astype(np.float32)

# -------------------------
# BUILD FAISS INDEX
# -------------------------

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# -------------------------
# SAVE VECTOR STORE
# -------------------------

VECTOR_STORE_DIR.mkdir(exist_ok=True)

faiss.write_index(index, str(VECTOR_STORE_DIR / "awsense.index"))

# -------------------------
# SAVE DOCUMENT METADATA
# -------------------------

with open(VECTOR_STORE_DIR / "documents.pkl", "wb") as f:
    pickle.dump(
        {
            "documents": documents,
            "sources": sources
        },
        f
    )

print("Vector DB created successfully")
