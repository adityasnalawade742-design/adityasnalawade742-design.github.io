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

asin = "B0C2YLN3H4"
winner_photo_url = "https://m.media-amazon.com/images/I/714vUVy9IDL._AC_SL1500_.jpg"

registry_file = project_root / "product_price_registry.json"
with open(registry_file, "r", encoding="utf-8") as f:
    reg = json.load(f)

pdata = reg[asin]
reg[asin]["subtitle"] = ""

print("==========================================")
print(f"Processing Donut Vases B0C2YLN3H4 with TRUE 1-Scene Photo...")
print(f"Winner Photo: {winner_photo_url}")

# 1. Master Vision Prompt
master_prompt = generate_cozy_image_prompt(
    product_title=pdata["title"],
    category="vase",
    key_features=", ".join(pdata["features"]),
    is_white_background=False
)

# 2. Run Replicate FLUX-Dev Img2Img with TRUE 1-Scene Winner Photo (prompt_strength = 0.35)
generated_img_path = generate_cozy_image(
    prompt=master_prompt,
    filename_prefix=f"raw_{asin}",
    real_image_url=winner_photo_url,
    init_image_path=winner_photo_url,
    prompt_strength=0.35
)

if generated_img_path and Path(generated_img_path).exists():
    raw_target = raw_dir / f"raw_{asin}.jpg"
    shutil.copy(generated_img_path, raw_target)
    reg[asin]["raw_image"] = f"raw_images/raw_{asin}.jpg"
    print(f"Saved True 1-Scene AI room photo to {raw_target.name}")
    
    # 3. Render Playwright 1200x1600 Text Template Overlay with blank subtitle
    hook_path = project_root / "focus_product_B0C2YLN3H4_exact2vases_hook.jpg"
    render_html_overlay(
        image_path=str(raw_target),
        headline=pdata["headline"],
        subtitle="",
        badge_text=pdata["badge"],
        price_str=pdata["current_price"],
        features=pdata["features"],
        output_path=str(hook_path),
        theme="bottom_glass_card"
    )
    shutil.copy(hook_path, project_root / "output" / "images" / hook_path.name)
    print(f"Rendered Playwright text template overlay to {hook_path.name}")

# Save registry
with open(registry_file, "w", encoding="utf-8") as f:
    json.dump(reg, f, indent=2)

print("\nSUCCESSFULLY PROCESSED B0C2YLN3H4 WITH TRUE 1-SCENE PHOTO!")
