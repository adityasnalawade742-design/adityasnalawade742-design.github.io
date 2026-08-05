import json
import sys
from pathlib import Path
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path(__file__).resolve().parent
raw_dir = repo / "raw_images"
reg_file = repo / "product_price_registry.json"

registry = json.loads(reg_file.read_text(encoding="utf-8"))

print(f"{'ASIN':<12} | {'Dimensions':<12} | {'Aspect Ratio':<12} | {'Product Title'}")
print("-" * 80)

for asin, item in registry.items():
    raw_path = raw_dir / f"raw_{asin}.jpg"
    if raw_path.exists():
        with Image.open(raw_path) as im:
            w, h = im.size
            ratio = f"{w/h:.2f}"
            print(f"{asin:<12} | {w}x{h:<7} | {ratio:<12} | {item.get('title', '')[:40]}")
    else:
        print(f"{asin:<12} | MISSING      | N/A          | {item.get('title', '')[:40]}")
