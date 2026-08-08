import sys
import io
import json
import shutil
from pathlib import Path
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_dir))

from modules.html_overlay_engine import render_html_overlay

soup = BeautifulSoup(open(repo_dir / "index.html", encoding="utf-8").read(), "html.parser")
cards = soup.find_all(class_="card-wrapper")
asins = [c.get("id").replace("card-", "") for c in cards]

registry = json.load(open(repo_dir / "product_price_registry.json", encoding="utf-8"))

flux_dir = repo_dir / "flux_clean_images"

print("==================================================")
print(f"🎨 RE-BUILDING {len(asins)} PRICE OVERLAY BADGES FROM CLEAN FLUX DEV IMAGES")
print("==================================================")

success_count = 0
for idx, asin in enumerate(asins, 1):
    meta = registry.get(asin, {})
    title = meta.get("title", f"Product {asin}")
    price = meta.get("current_price", "$19.99")
    features = meta.get("features", ["VIRAL ROOM DECOR", "COZY VIBE", "HIGH QUALITY"])
    
    # Priority 1: Check flux_clean_images/
    flux_candidates = [
        flux_dir / f"clean_focus_product_{asin}.jpg",
        flux_dir / f"clean_{asin}.jpg",
        flux_dir / f"focus_product_{asin}.jpg",
        flux_dir / f"focus_product_{asin}_ai.jpg",
        flux_dir / f"flux_{asin}.jpg"
    ]
    
    clean_img = None
    for cand in flux_candidates:
        if cand.exists():
            clean_img = cand
            break
            
    if not clean_img:
        clean_img = repo_dir / "raw_images" / f"raw_{asin}.jpg"
        
    if not clean_img.exists():
        print(f"[{idx}/{len(asins)}] ⚠️ Skipping {asin}: No clean image found")
        continue

    hook_name = f"focus_product_{asin}_hook.jpg"
    output_path = repo_dir / hook_name

    print(f"\n[{idx}/{len(asins)}] ASIN: {asin} - '{title[:40]}...'")
    print(f"  └─ Background: {clean_img.name}")
    print(f"  └─ Price Tag:  {price}")

    try:
        render_html_overlay(
            image_path=str(clean_img),
            headline=title[:45],
            subtitle="COZY HOME & LUXURY ROOM FIND",
            badge_text="✨ VIRAL ROOM FIND",
            price_str=price,
            features=features[:3],
            output_path=str(output_path),
            theme="bottom_glass_card"
        )
        
        # Copy to output/images/
        out_img = repo_dir / "output" / "images" / hook_name
        out_img.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(output_path, out_img)
        success_count += 1
        print(f"  ✅ Re-rendered price graphic badge successfully: {hook_name}")

    except Exception as e:
        print(f"  ❌ Error re-rendering overlay for {asin}: {e}")

print("==================================================")
print(f"🎉 SUCCESS: Re-rendered {success_count} / {len(asins)} price overlay graphic badges from clean Flux images!")
print("==================================================")
