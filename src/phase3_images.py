import json
from pathlib import Path
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from tqdm import tqdm

# ----------------------------
# CONFIG
# ----------------------------
IMAGE_ELEMENTS_FILE = Path("data/phase2_routed/image_elements.json")
OUTPUT_DIR = Path("data/phase3_images")
OUTPUT_FILE = OUTPUT_DIR / "image_captions.json"

MODEL_NAME = "Salesforce/blip-image-captioning-base"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------
# LOAD MODEL
# ----------------------------
print("🔹 Loading BLIP model...")

processor = BlipProcessor.from_pretrained(MODEL_NAME)
model = BlipForConditionalGeneration.from_pretrained(MODEL_NAME)
model.eval()

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

print(f"✅ BLIP model loaded on {device}")

# ----------------------------
# CAPTIONING FUNCTION
# ----------------------------
def generate_caption(image_path: Path) -> str:
    try:
        image = Image.open(image_path).convert("RGB")
    except Exception as e:
        print(f"❌ Failed to open image {image_path}: {e}")
        return ""

    # IMPORTANT: NO PROMPT
    inputs = processor(image, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    try:
        with torch.no_grad():
            output = model.generate(**inputs, max_new_tokens=50)

        caption = processor.decode(
            output[0],
            skip_special_tokens=True
        )
        return caption

    except Exception as e:
        print(f"❌ Caption generation failed for {image_path}: {e}")
        return ""

# ----------------------------
# MAIN
# ----------------------------
def main():
    if not IMAGE_ELEMENTS_FILE.exists():
        raise FileNotFoundError(f"{IMAGE_ELEMENTS_FILE} not found")

    with open(IMAGE_ELEMENTS_FILE, "r", encoding="utf-8") as f:
        image_elements = json.load(f)

    captions = []

    print(f"🖼️ Generating captions for {len(image_elements)} images...")

    for el in tqdm(image_elements, desc="Captioning images"):
        image_path_str = el["metadata"].get("image_path")
        if not image_path_str:
            continue

        image_path = Path(image_path_str)
        caption = generate_caption(image_path)

        captions.append({
            "element_id": el["element_id"],
            "page_number": el["metadata"]["page_number"],
            "image_path": str(image_path),
            "existing_text": el.get("text"),
            "blip_caption": caption
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(captions, f, indent=2, ensure_ascii=False)

    print(f"✅ Phase 3 captions saved to: {OUTPUT_FILE}")

# ----------------------------
# ENTRY POINT
# ----------------------------
if __name__ == "__main__":
    main()
