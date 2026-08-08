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

asin = "B0BYP7XB7S"
title = "LCCCK White and Silver Ceramic Vases for Home Decor"
category = "vases"
features = ["SILVER ACCENT RING", "SET OF 2 VASES", "MATTE CERAMIC GRAIN", "PAMPAS GRASS READY"]

input_image = repo_dir / "scratch" / "B0BYP7XB7S_candidates" / "option_4.jpg"
if not input_image.exists():
    input_image = "https://m.media-amazon.com/images/I/71k74vcuhjL._AC_SL1500_.jpg"
else:
    input_image = str(input_image)

prompt = generate_cozy_image_prompt(
    product_title=title,
    category=category,
    key_features=features,
    is_white_background=False
)

strength = 0.30

print("==================================================")
print(f"🎨 RE-RENDERING CLEAN FLUX-DEV IMAGE FOR {asin}")
print(f"📌 Input Reference: Photo 4 ({input_image})")
print(f"📌 Selected Precision Strength: {strength}")
print(f"💬 Prompt: {prompt}")
print("==================================================")

out_path = generate_cozy_image(
    prompt=prompt,
    filename_prefix=f"focus_product_{asin}",
    init_image_path=input_image,
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
    print(f"✅ Saved re-rendered Flux Dev image (strength=0.30) to: {clean_target.name}")

print("==================================================")
