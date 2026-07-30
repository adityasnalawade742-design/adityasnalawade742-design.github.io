import os
import sys
from pathlib import Path
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")

print("==================================================")
print("⚡ STEP 1: COMPRESSING ALL GRAPHIC IMAGES FOR SPEED")
print("==================================================")

hook_imgs = list(repo_dir.glob("focus_product_*_hook.jpg"))
total_before = 0
total_after = 0

for img_path in hook_imgs:
    size_before = img_path.stat().st_size
    total_before += size_before
    
    with Image.open(img_path) as im:
        # Convert to RGB and save optimized JPEG
        im.convert("RGB").save(img_path, "JPEG", quality=85, optimize=True)
        
    size_after = img_path.stat().st_size
    total_after += size_after
    
    saved_pct = round((1 - (size_after / size_before)) * 100, 1)
    print(f" 🖼️ {img_path.name}: {round(size_before/1024, 1)} KB ➔ {round(size_after/1024, 1)} KB (Saved {saved_pct}%)")

print("\n--------------------------------------------------")
mb_saved = round((total_before - total_after) / (1024 * 1024), 2)
pct_saved = round((1 - (total_after / total_before)) * 100, 1)
print(f"🎉 TOTAL PAYLOAD SAVED: {mb_saved} MB ({pct_saved}% Reduction!)")
print("==================================================")
