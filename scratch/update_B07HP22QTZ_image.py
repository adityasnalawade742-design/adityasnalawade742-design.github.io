import sys
import os
import json
import urllib.request
import shutil
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_dir))

from config import REPLICATE_API_TOKEN
from modules.vision_prompt import generate_cozy_image_prompt
from modules.image_generator import generate_cozy_image
from modules.amazon_extractor import calculate_precision_prompt_strength

asin = "B07HP22QTZ"
title = "Hanging Crystal Suncatcher Prism"
category = "decor"
features = ["CRYSTAL PRISM CLUSTER", "RAINBOW LIGHT REFLECTION", "WINDOW SUNCATCHER", "HANDMADE GLASS"]

new_raw_url = "https://m.media-amazon.com/images/I/61iGoWzpwmL._AC_SL1000_.jpg"

# 1. Save new raw image
raw_dir = repo_dir / "raw_images"
raw_dir.mkdir(exist_ok=True)
raw_file = raw_dir / f"raw_{asin}.jpg"

print(f"📥 Downloading new raw image for {asin} from: {new_raw_url}...")
headers = {"User-Agent": "Mozilla/5.0"}
req = urllib.request.Request(new_raw_url, headers=headers)
img_data = urllib.request.urlopen(req, timeout=12).read()
raw_file.write_bytes(img_data)
print(f"✅ Saved raw image: {raw_file.name} ({len(img_data)/1024:.1f} KB)")

# 2. Compute dynamic precision strength (0.28 for suncatcher crystals)
prompt = generate_cozy_image_prompt(
    product_title=title,
    category=category,
    key_features=features,
    is_white_background=False
)

strength = calculate_precision_prompt_strength(title, is_white_bg=False)
if strength > 0.30:
    strength = 0.28  # Keep crystal cluster shape precise

print("==================================================")
print(f"🎨 GENERATING CLEAN FLUX-DEV IMAGE FOR {asin}")
print(f"📌 Input Reference: {raw_file.name}")
print(f"📌 Dynamic Precision Strength: {strength}")
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
    print(f"✅ Saved clean Flux Dev image to: {clean_target.name}")

print("==================================================")
