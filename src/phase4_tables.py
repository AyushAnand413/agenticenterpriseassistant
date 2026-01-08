import json
from pathlib import Path
import re

# ----------------------------
# CONFIG
# ----------------------------
INPUT_FILE = Path("data/phase2_routed/table_elements.json")
OUTPUT_DIR = Path("data/phase4_tables")

RAW_TABLES_FILE = OUTPUT_DIR / "raw_tables.json"
NORMALIZED_TABLES_FILE = OUTPUT_DIR / "normalized_tables.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------
# NORMALIZATION LOGIC
# ----------------------------
def normalize_table_text(table_text: str):
    """
    Conservative normalization for retrieval.
    Does NOT assume row structure.
    Does NOT invent headers.
    """
    if not table_text:
        return []

    # Normalize whitespace
    clean_text = re.sub(r"\s+", " ", table_text).strip()

    if len(clean_text) < 20:
        return []

    # Create ONE safe retrievable sentence
    return [
        f"The table contains the following information: {clean_text}."
    ]


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"{INPUT_FILE} not found")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        tables = json.load(f)

    raw_tables = []
    normalized_tables = []

    for table in tables:
        raw_text = table.get("text", "")

        raw_tables.append({
            "element_id": table["element_id"],
            "page_number": table["metadata"]["page_number"],
            "raw_text": raw_text
        })

        normalized_sentences = normalize_table_text(raw_text)

        for sentence in normalized_sentences:
            normalized_tables.append({
                "element_id": table["element_id"],
                "page_number": table["metadata"]["page_number"],
                "normalized_text": sentence
            })

    with open(RAW_TABLES_FILE, "w", encoding="utf-8") as f:
        json.dump(raw_tables, f, indent=2, ensure_ascii=False)

    with open(NORMALIZED_TABLES_FILE, "w", encoding="utf-8") as f:
        json.dump(normalized_tables, f, indent=2, ensure_ascii=False)

    print("✅ Phase 4 table processing complete")
    print(f"Raw tables       : {len(raw_tables)}")
    print(f"Normalized rows  : {len(normalized_tables)}")


if __name__ == "__main__":
    main()
