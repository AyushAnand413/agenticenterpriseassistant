import json
import logging
from pathlib import Path
from unstructured.partition.pdf import partition_pdf

logging.getLogger("pdfminer").setLevel(logging.ERROR)

# ----------------------------
# CONFIG
# ----------------------------
INPUT_PDF = Path("data/input/poa_sample.pdf")
OUTPUT_DIR = Path("data/phase1_parsed")
OUTPUT_FILE = OUTPUT_DIR / "elements_raw.json"

FIGURES_DIR = Path("figures")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------
# PHASE 1: PARSE PDF
# ----------------------------
def parse_pdf(pdf_path: Path):
    """
    Parses PDF into ordered Unstructured elements.
    No transformation, no interpretation.
    """
    return partition_pdf(
        filename=str(pdf_path),
        extract_images_in_pdf=True,
        infer_table_structure=True,
        chunking_strategy=None
    )


def serialize_elements(elements, source_file: str, figure_paths):
    """
    Convert Unstructured elements into JSON-serializable dicts
    and attach image paths deterministically.
    """
    serialized = []
    image_idx = 0

    for idx, el in enumerate(elements):
        metadata = {
            "page_number": el.metadata.page_number,
            "source_file": source_file,
            "coordinates": (
                el.metadata.coordinates.to_dict()
                if el.metadata.coordinates
                else None
            )
        }

        if el.category == "Image":
            metadata["image_path"] = (
                str(figure_paths[image_idx])
                if image_idx < len(figure_paths)
                else None
            )
            image_idx += 1

        serialized.append({
            "element_id": idx,
            "element_type": el.category,
            "element_class": el.__class__.__name__,
            "text": el.text,
            "metadata": metadata
        })

    return serialized


def main():
    if not INPUT_PDF.exists():
        raise FileNotFoundError(f"PDF not found: {INPUT_PDF}")

    # Parse FIRST (this creates figures/)
    print("🔹 Parsing PDF...")
    elements = parse_pdf(INPUT_PDF)
    print(f"🔹 Parsed {len(elements)} elements")

    if not FIGURES_DIR.exists():
        raise FileNotFoundError("Figures directory not found after parsing")

    # Collect figures AFTER parsing
    figure_paths = sorted(
        p for p in FIGURES_DIR.iterdir()
        if p.suffix.lower() in {".png", ".jpg", ".jpeg"}
    )

    print(f"🔹 Found {len(figure_paths)} extracted images")

    serialized_elements = serialize_elements(
        elements,
        source_file=INPUT_PDF.name,
        figure_paths=figure_paths
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(serialized_elements, f, indent=2, ensure_ascii=False)

    print(f"✅ Phase 1 output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
