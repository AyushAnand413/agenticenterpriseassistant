import json
from pathlib import Path
from collections import defaultdict

# ----------------------------
# CONFIG
# ----------------------------
TEXT_FILE = Path("data/phase2_routed/text_elements.json")
IMAGE_CAPTIONS_FILE = Path("data/phase3_images/image_captions.json")
TABLES_FILE = Path("data/phase4_tables/normalized_tables.json")

OUTPUT_DIR = Path("data/phase5_chunks")
OUTPUT_FILE = OUTPUT_DIR / "chunks.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------
# HELPERS
# ----------------------------
def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"{path} not found")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ----------------------------
# MAIN
# ----------------------------
def main():
    text_elements = load_json(TEXT_FILE)
    image_captions = load_json(IMAGE_CAPTIONS_FILE)
    table_rows = load_json(TABLES_FILE)

    # Index images and tables by page
    images_by_page = defaultdict(list)
    for img in image_captions:
        images_by_page[img["page_number"]].append(img)

    tables_by_page = defaultdict(list)
    for tbl in table_rows:
        tables_by_page[tbl["page_number"]].append(tbl)

    chunks = []
    current_chunk = None

    attached_images = set()
    attached_tables = set()

    for el in text_elements:
        el_type = el["element_type"]
        page = el["metadata"]["page_number"]
        text = (el.get("text") or "").strip()

        # ----------------------------
        # Start new chunk on Title
        # ----------------------------
        if el_type == "Title":
            if current_chunk:
                chunks.append(current_chunk)

            current_chunk = {
                "title": text,
                "content": [],
                "pages": set(),
                "sources": {
                    "text_elements": [],
                    "image_elements": [],
                    "table_elements": []
                }
            }

            attached_images = set()
            attached_tables = set()

            # IMPORTANT: record page even if body not yet added
            current_chunk["pages"].add(page)

            continue

        # ----------------------------
        # Handle pre-title content
        # ----------------------------
        if current_chunk is None:
            current_chunk = {
                "title": "Document Introduction",
                "content": [],
                "pages": set(),
                "sources": {
                    "text_elements": [],
                    "image_elements": [],
                    "table_elements": []
                }
            }

        # Always record page
        current_chunk["pages"].add(page)

        # ----------------------------
        # Attach images ONCE per chunk
        # ----------------------------
        for img in images_by_page.get(page, []):
            if img["element_id"] not in attached_images:
                current_chunk["content"].append(
                    f"[Image Description]: {img['blip_caption']}"
                )
                current_chunk["sources"]["image_elements"].append(img["element_id"])
                attached_images.add(img["element_id"])

        # ----------------------------
        # Attach tables ONCE per chunk
        # ----------------------------
        for tbl in tables_by_page.get(page, []):
            if tbl["element_id"] not in attached_tables:
                current_chunk["content"].append(
                    f"[Table Information]: {tbl['normalized_text']}"
                )
                current_chunk["sources"]["table_elements"].append(tbl["element_id"])
                attached_tables.add(tbl["element_id"])

        # ----------------------------
        # Add narrative text
        # ----------------------------
        if text:
            current_chunk["content"].append(text)
            current_chunk["sources"]["text_elements"].append(el["element_id"])

    if current_chunk:
        chunks.append(current_chunk)

    # ----------------------------
    # FINAL SERIALIZATION
    # ----------------------------
    final_chunks = []
    for idx, ch in enumerate(chunks):
        final_chunks.append({
            "chunk_id": idx,
            "title": ch["title"],
            "text": "\n".join(ch["content"]),
            "pages": sorted(ch["pages"]),
            "sources": ch["sources"]
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_chunks, f, indent=2, ensure_ascii=False)

    print("✅ Phase 5 chunking complete")
    print(f"Total chunks created: {len(final_chunks)}")

# ----------------------------
# ENTRY
# ----------------------------
if __name__ == "__main__":
    main()
