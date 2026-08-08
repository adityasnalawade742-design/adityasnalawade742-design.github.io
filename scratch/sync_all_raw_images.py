import sys
import io
import json
import urllib.request
import re
from pathlib import Path
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent
raw_dir = repo_dir / "raw_images"
raw_dir.mkdir(exist_ok=True)

flux_dir = repo_dir / "flux_clean_images"

# Remove old orphan file focus_product_B0BPNXX2MF_ai.jpg
orphan = flux_dir / "focus_product_B0BPNXX2MF_ai.jpg"
if orphan.exists():
    orphan.unlink()
    print(f"Cleaned orphan file: {orphan.name}")

# Check homepage active ASINs
soup = BeautifulSoup(open(repo_dir / "index.html", encoding="utf-8").read(), "html.parser")
cards = soup.find_all(class_="card-wrapper")
active_asins = [c.get("id").replace("card-", "") for c in cards]

registry = json.load(open(repo_dir / "product_price_registry.json", encoding="utf-8"))

headers = {"User-Agent": "Mozilla/5.0"}
for asin in active_asins:
    raw_file = raw_dir / f"raw_{asin}.jpg"
    if not raw_file.exists():
        meta = registry.get(asin, {})
        img_url = meta.get("image_path") or meta.get("image_url") or f"https://m.media-amazon.com/images/I/71+K2WB572L._AC_SL1500_.jpg"
        if not img_url.startswith("http"):
            img_url = f"https://m.media-amazon.com/images/I/71+K2WB572L._AC_SL1500_.jpg"
        try:
            req = urllib.request.Request(img_url, headers=headers)
            data = urllib.request.urlopen(req, timeout=10).read()
            raw_file.write_bytes(data)
            print(f"Downloaded raw image for ASIN {asin}: {raw_file.name}")
        except Exception as e:
            print(f"Error downloading raw for {asin}: {e}")

raw_files = list(raw_dir.glob("*.jpg"))
clean_files = list(flux_dir.glob("*.jpg"))

print("==================================================")
print(f"📦 Active Storefront Homepage Products: {len(active_asins)}")
print(f"🖼️ Raw Seller Source Images (raw_images/): {len(raw_files)}")
print(f"🎨 Clean Flux Dev AI Images (flux_clean_images/): {len(clean_files)}")
print("==================================================")
