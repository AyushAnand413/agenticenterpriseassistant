import json
from pathlib import Path
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ----------------------------
# CONFIG
# ----------------------------
FAISS_INDEX_FILE = Path("data/embeddings/faiss.index")
METADATA_FILE = Path("data/embeddings/metadata.json")
CHUNKS_FILE = Path("data/phase5_chunks/chunks.json")

EMBED_MODEL = "BAAI/bge-small-en"
TOP_K = 5

# ----------------------------
# LOAD ARTIFACTS
# ----------------------------
print("🔹 Loading FAISS index...")
index = faiss.read_index(str(FAISS_INDEX_FILE))

with open(METADATA_FILE, "r", encoding="utf-8") as f:
    metadata = json.load(f)

with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print("🔹 Loading embedding model...")
model = SentenceTransformer(EMBED_MODEL)

# ----------------------------
# RETRIEVAL FUNCTION
# ----------------------------
def retrieve(query: str, top_k: int = TOP_K):
    query_embedding = model.encode(
    [f"Represent this sentence for searching relevant passages: {query}"],
    convert_to_numpy=True,
    normalize_embeddings=True
    )

    scores, indices = index.search(query_embedding, top_k)

    results = []
    for rank, idx in enumerate(indices[0]):
        if idx == -1:
            continue

        chunk = chunks[idx]
        results.append({
            "rank": rank + 1,
            "title": chunk["title"],
            "pages": chunk["pages"],
            "text_preview": chunk["text"][:500] + "..."
        })

    return results

# ----------------------------
# DEMO LOOP
# ----------------------------
if __name__ == "__main__":
    print("\n🔍 Retrieval-only mode (no LLM)")
    print("Type 'exit' to quit.\n")

    while True:
        query = input(" Query: ").strip()
        if query.lower() == "exit":
            break

        hits = retrieve(query)

        print("\n📄 Retrieved Sections:")
        for h in hits:
            print(f"\n🔹 Rank {h['rank']}")
            print(f"Title : {h['title']}")
            print(f"Pages : {h['pages']}")
            print(f"Preview:\n{h['text_preview']}")
