import json
import shutil
import requests
from pathlib import Path
from modules.vision_prompt import generate_cozy_image_prompt
from modules.image_generator import generate_cozy_image
from modules.html_overlay_engine import render_html_overlay

project_root = Path("G:/CLI/pinterest-auto-affiliate")
raw_dir = project_root / "raw_images"
raw_dir.mkdir(exist_ok=True)

asin = "B0FXLYXM32"
winner_photo_url = "https://m.media-amazon.com/images/I/81A-bdsnQtL._AC_SL1500_.jpg"

registry_file = project_root / "product_price_registry.json"
with open(registry_file, "r", encoding="utf-8") as f:
    reg = json.load(f)

pdata = reg[asin]
print(f"==========================================")
print(f"Processing Product 1: {asin} ({pdata['headline']})...")
print(f"Winner Photo: {winner_photo_url}")

# 1. Master Vision Prompt from modules/vision_prompt.py
master_prompt = generate_cozy_image_prompt(
    product_title=pdata["title"],
    category="mirror",
    key_features=", ".join(pdata["features"]),
    is_white_background=False
)

print(f"Master Vision Prompt: {master_prompt[:120]}...")

# 2. Run AI Img2Img Room Generator (strength=0.40)
generated_img_path = generate_cozy_image(
    prompt=master_prompt,
    filename_prefix=f"raw_{asin}",
    real_image_url=winner_photo_url,
    prompt_strength=0.40
)

if generated_img_path and Path(generated_img_path).exists():
    raw_target = raw_dir / f"raw_{asin}.jpg"
    shutil.copy(generated_img_path, raw_target)
    reg[asin]["raw_image"] = f"raw_images/raw_{asin}.jpg"
    print(f"✓ Saved clean AI room photo to {raw_target.name}")
    
    # 3. Render Playwright 1200x1600 Text Template Overlay
    hook_path = project_root / f"focus_product_{asin}_hook.jpg"
    render_html_overlay(
        image_path=str(raw_target),
        headline=pdata["headline"],
        subtitle=pdata["subtitle"],
        badge_text=pdata["badge"],
        price_str=pdata["current_price"],
        features=pdata["features"],
        output_path=str(hook_path),
        theme="bottom_glass_card"
    )
    shutil.copy(hook_path, project_root / "output" / "images" / hook_path.name)
    print(f"✓ Re-rendered Playwright text template overlay to {hook_path.name}")

# Save registry
with open(registry_file, "w", encoding="utf-8") as f:
    json.dump(reg, f, indent=2)

print("\nSUCCESSFULLY PROCESSED & RENDERED B0FXLYXM32!")
