import os
import json
import sys
from pathlib import Path
from PIL import Image, ImageStat

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path(__file__).resolve().parent
raw_dir = repo / "raw_images"
reg_file = repo / "product_price_registry.json"

registry = json.loads(reg_file.read_text(encoding="utf-8"))

print(f"{'Filename':<22} | {'ASIN':<10} | {'Dimensions':<11} | {'Size (KB)':<10} | {'White %':<8} | {'Type Classification'}")
print("=" * 95)

for f in sorted(raw_dir.glob("raw_*.jpg")):
    filename = f.name
    asin = filename.replace("raw_", "").replace(".jpg", "")
    size_kb = f.stat().st_size / 1024
    
    with Image.open(f) as im:
        w, h = im.size
        # Sample image to analyze background
        im_rgb = im.convert("RGB")
        stat = ImageStat.Stat(im_rgb)
        
        # Count near-white pixels (R>245, G>245, B>245)
        # Resize to 100x100 for fast pixel analysis
        small = im_rgb.resize((100, 100))
        pixels = list(small.getdata())
        white_count = sum(1 for r, g, b in pixels if r > 240 and g > 240 and b > 240)
        white_pct = (white_count / len(pixels)) * 100
        
        if white_pct > 40:
            classification = "⚪ Amazon White Studio Photo"
        else:
            classification = "✨ Flux Dev AI Lifestyle Room Photo"
            
        print(f"{filename:<22} | {asin:<10} | {w}x{h:<6} | {size_kb:<9.1f} | {white_pct:<7.1f}% | {classification}")

print("=" * 95)
