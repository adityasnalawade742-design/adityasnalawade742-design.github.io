import sys
import os
import json
import shutil
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_dir))

from config import REPLICATE_API_TOKEN
from modules.vision_prompt import generate_cozy_image_prompt
from modules.image_generator import generate_cozy_image

asin = "B0GYDXHF4G"
title = "Flame Aroma Essential Oil Diffuser Dark Crackle"
category = "decor"
features = ["VOLCANO FLAME MIST", "WARM AMBER GLOW", "AUTO SHUT OFF", "ESSENTIAL OIL READY"]

input_image = repo_dir / "raw_images" / "raw_B0GYDXHF4G.jpg"
if not input_image.exists():
    raise FileNotFoundError(f"Input image missing: {input_image}")

input_image_str = str(input_image)

prompt = generate_cozy_image_prompt(
    product_title=title,
    category=category,
    key_features=features,
    is_white_background=False
)

strength = 0.44

print("==================================================")
print(f"🎨 GENERATING CLEAN FLUX-DEV IMAGE FOR {asin}")
print(f"📌 Input Reference: raw_images/raw_B0GYDXHF4G.jpg")
print(f"📌 Selected Precision Strength: {strength}")
print(f"💬 Prompt: {prompt}")
print("==================================================")

out_path = generate_cozy_image(
    prompt=prompt,
    filename_prefix=f"focus_product_{asin}",
    init_image_path=input_image_str,
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
    print(f"✅ Saved clean Flux Dev image (strength=0.44) to: {clean_target.name}")

print("==================================================")
