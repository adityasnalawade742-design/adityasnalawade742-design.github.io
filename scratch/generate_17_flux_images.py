import sys
import os
import json
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_dir))

from config import REPLICATE_API_TOKEN
from modules.vision_prompt import generate_cozy_image_prompt
from modules.image_generator import generate_cozy_image

registry_file = repo_dir / "product_price_registry.json"
with open(registry_file, "r", encoding="utf-8") as f:
    registry = json.load(f)

flux_dir = repo_dir / "flux_clean_images"
flux_dir.mkdir(exist_ok=True)

raw_dir = repo_dir / "raw_images"

homepage_asins = [
    "B0BYP7XB7S", "B0FFG48KCY", "B0DC6HDMRM", "B0BPM41R5C", "B0D5YNHXQ7",
    "B0D6YRJLCP", "B0BXP7YWHJ", "B0C7WFZZ7D", "B0BQGC76VX", "B0CJC549C6",
    "B0GYDXHF4G", "B0FXLYXM32", "B0C2YLN3H4", "B0BZXNSW5K", "B0DXKGL1T2",
    "B0D1FRDFFX", "B0D8P8CSYP"
]

# Find ASINs missing clean Flux images
missing_asins = []
for asin in homepage_asins:
    existing = list(flux_dir.glob(f"*{asin}*"))
    if not existing:
        missing_asins.append(asin)

print("==================================================")
print(f"🚀 GENERATING {len(missing_asins)} REMAINING CLEAN FLUX-DEV IMAGES (WITH 12s RATE-LIMIT DELAY)")
print(f"📌 Missing ASINs: {missing_asins}")
print("==================================================")

for idx, asin in enumerate(missing_asins, 1):
    meta = registry.get(asin, {})
    title = meta.get("title", f"Product {asin}")
    category = meta.get("category", "decor")
    features = meta.get("features", [])

    raw_path = raw_dir / f"raw_{asin}.jpg"
    if not raw_path.exists():
        print(f"\n[{idx}/{len(missing_asins)}] ⚠️ Skipping ASIN {asin}: raw image missing at {raw_path.name}")
        continue

    prompt = generate_cozy_image_prompt(
        product_title=title,
        category=category,
        key_features=features,
        is_white_background=False
    )

    from modules.amazon_extractor import calculate_precision_prompt_strength
    strength = calculate_precision_prompt_strength(title, is_white_bg=False)

    print(f"\n--------------------------------------------------")
    print(f"🎨 [{idx}/{len(missing_asins)}] ASIN: {asin} - {title[:45]}")
    print(f"📌 Model: black-forest-labs/flux-dev | Dynamic Strength: {strength}")
    print(f"💬 Prompt: {prompt[:120]}...")

    try:
        out_path = generate_cozy_image(
            prompt=prompt,
            filename_prefix=f"focus_product_{asin}",
            init_image_path=str(raw_path),
            prompt_strength=strength
        )
        print(f" ✅ Saved Clean Flux Image: {out_path}")
    except Exception as e:
        print(f" ⚠️ Error rendering Flux Dev for {asin}: {e}")

    if idx < len(missing_asins):
        print(f" ⏳ Waiting 12 seconds to respect Replicate rate limits...")
        time.sleep(12)

print("\n==================================================")
print(f"🎉 REMAINING FLUX-DEV GENERATION COMPLETE!")
print("==================================================")
