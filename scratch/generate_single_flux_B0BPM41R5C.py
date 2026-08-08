import sys
import os
import json
import shutil
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_dir))

from config import REPLICATE_API_TOKEN
from modules.vision_prompt import generate_cozy_image_prompt
from modules.image_generator import generate_cozy_image
from modules.amazon_extractor import calculate_precision_prompt_strength

asin = "B0BPM41R5C"
title = "Ceramic Hand Sculpture Ring Holder"
category = "decor"
features = ["CERAMIC HAND SCULPTURE", "RING & JEWELRY HOLDER", "BOHO AESTHETIC", "MATTE CERAMIC GRAIN"]

input_image = repo_dir / "scratch" / "B0BPM41R5C_candidates" / "option_7.jpg"
if not input_image.exists():
    input_image = "https://m.media-amazon.com/images/I/81V0VI3YMmL._AC_SL1500_.jpg"
else:
    input_image = str(input_image)

# Update raw seller image in raw_images/
raw_dir = repo_dir / "raw_images"
raw_dir.mkdir(exist_ok=True)
raw_file = raw_dir / f"raw_{asin}.jpg"
if Path(input_image).exists():
    shutil.copy(input_image, raw_file)
    print(f"✅ Updated raw seller image: {raw_file.name}")

prompt = generate_cozy_image_prompt(
    product_title=title,
    category=category,
    key_features=features,
    is_white_background=False
)

strength = 0.48

print("==================================================")
print(f"🎨 GENERATING CLEAN FLUX-DEV IMAGE FOR {asin}")
print(f"📌 Input Reference: Option 7 ({input_image})")
print(f"📌 Selected Precision Strength: {strength}")
print(f"💬 Prompt: {prompt}")
print("==================================================")

out_path = generate_cozy_image(
    prompt=prompt,
    filename_prefix=f"focus_product_{asin}",
    init_image_path=str(raw_file),
    prompt_strength=strength
)

flux_dir = repo_dir / "flux_clean_images"
flux_dir.mkdir(exist_ok=True)
clean_target = flux_dir / f"clean_focus_product_{asin}.jpg"

if Path(out_path).exists():
    shutil.copy(out_path, clean_target)
    
    # Also copy to artifact directory
    artifact_dir = Path(r"C:\Users\adity\.gemini\antigravity-cli\brain\663690f5-e7a9-486f-8df0-99811c14b2b0")
    artifact_target = artifact_dir / f"clean_focus_product_{asin}.jpg"
    shutil.copy(out_path, artifact_target)
    print(f"✅ Saved clean Flux Dev image (strength=0.48) to: {clean_target.name}")

print("==================================================")
