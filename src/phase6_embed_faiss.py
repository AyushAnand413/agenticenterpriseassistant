import json
from pathlib import Path
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ----------------------------
# CONFIG
# ----------------------------
CHUNKS_FILE = Path("data/phase5_chunks/chunks.json")

OUTPUT_DIR = Path("data/embeddings")
FAISS_INDEX_FILE = OUTPUT_DIR / "faiss.index"
METADATA_FILE = OUTPUT_DIR / "metadata.json"

EMBED_MODEL = "BAAI/bge-small-en"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------
# LOAD DATA
# ----------------------------
with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [c["text"] for c in chunks]

metadata = [
    {
        "chunk_id": c["chunk_id"],
        "title": c["title"],
        "pages": c["pages"]
    }
    for c in chunks
]

# ----------------------------
# EMBEDDINGS
# ----------------------------
print("🔹 Loading embedding model...")
model = SentenceTransformer(EMBED_MODEL)

print("🔹 Generating embeddings...")
embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    normalize_embeddings=True,
    show_progress_bar=True
)

dim = embeddings.shape[1]

# ----------------------------
# FAISS INDEX
# ----------------------------
print("🔹 Building FAISS index...")
index = faiss.IndexFlatIP(dim)  # cosine similarity
index.add(embeddings)

# ----------------------------
# SAVE
# ----------------------------
faiss.write_index(index, str(FAISS_INDEX_FILE))

with open(METADATA_FILE, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print("✅ Embeddings + FAISS index created")
print(f"Total vectors indexed: {index.ntotal}")
