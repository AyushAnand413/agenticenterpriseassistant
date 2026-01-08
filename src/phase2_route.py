import json
from pathlib import Path

# ----------------------------
# CONFIG
# ----------------------------
INPUT_FILE = Path("data/phase1_parsed/elements_raw.json")
OUTPUT_DIR = Path("data/phase2_routed")

TEXT_FILE = OUTPUT_DIR / "text_elements.json"
TABLE_FILE = OUTPUT_DIR / "table_elements.json"
IMAGE_FILE = OUTPUT_DIR / "image_elements.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------
# ROUTING LOGIC
# ----------------------------
TEXT_TYPES = {
    "Title",
    "NarrativeText",
    "ListItem",
    "Header",
    "Footer"
}

TABLE_TYPES = {
    "Table"
}

IMAGE_TYPES = {
    "Image",
    "Figure"
}


def route_elements(elements):
    text_elements = []
    table_elements = []
    image_elements = []

    for el in elements:
        el_type = el.get("element_type")

        if el_type in TEXT_TYPES:
            text_elements.append(el)

        elif el_type in TABLE_TYPES:
            table_elements.append(el)

        elif el_type in IMAGE_TYPES:
            image_elements.append(el)

        else:
            # Fallback: treat unknown types as text
            text_elements.append(el)

    return text_elements, table_elements, image_elements


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input not found: {INPUT_FILE}")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        elements = json.load(f)

    text_elements, table_elements, image_elements = route_elements(elements)

    with open(TEXT_FILE, "w", encoding="utf-8") as f:
        json.dump(text_elements, f, indent=2, ensure_ascii=False)

    with open(TABLE_FILE, "w", encoding="utf-8") as f:
        json.dump(table_elements, f, indent=2, ensure_ascii=False)

    with open(IMAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(image_elements, f, indent=2, ensure_ascii=False)

    print("✅ Phase 2 routing complete")
    print(f"Text elements : {len(text_elements)}")
    print(f"Table elements: {len(table_elements)}")
    print(f"Image elements: {len(image_elements)}")


if __name__ == "__main__":
    main()
