import sys
from pathlib import Path
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")
candidates = [
    repo / "raw_images" / "raw_B0D8P8CSYP.jpg",
    repo / "raw_B0D8P8CSYP_console.jpg",
    repo / "focus_product_B0D8P8CSYP_hook_v2.jpg",
    repo / "focus_product_B0D8P8CSYP_hook.jpg"
]

print("==================================================")
print("🔍 CANDIDATE IMAGES FOR CUTE BIRD LAMP (B0D8P8CSYP)")
print("==================================================")

for c in candidates:
    if c.exists():
        img = Image.open(c)
        print(f" • {c.name:35s} | Size: {c.stat().st_size:8d} bytes | Res: {img.width}x{img.height}")
    else:
        print(f" • {c.name:35s} | Not Found")
