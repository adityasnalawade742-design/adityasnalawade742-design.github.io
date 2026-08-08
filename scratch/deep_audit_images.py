import sys
import io
import json
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent

# 1. Storefront index.html ASINs
index_path = repo_dir / "index.html"
soup = BeautifulSoup(open(index_path, encoding="utf-8").read(), "html.parser")
cards = soup.find_all(class_="card-wrapper")
index_asins = [c.get("id").replace("card-", "") for c in cards]

# 2. Registry ASINs
registry_path = repo_dir / "product_price_registry.json"
registry = json.load(open(registry_path, encoding="utf-8")) if registry_path.exists() else {}

# 3. Geo Matrix ASINs
matrix_path = repo_dir / "global_direct_matrix.json"
matrix = json.load(open(matrix_path, encoding="utf-8")) if matrix_path.exists() else {}

# 4. Raw files
raw_dir = repo_dir / "raw_images"
raw_files = {f.stem.replace("raw_", ""): f for f in raw_dir.glob("*.jpg")} if raw_dir.exists() else {}

# 5. Clean files
clean_dir = repo_dir / "flux_clean_images"
clean_files = {}
if clean_dir.exists():
    for f in clean_dir.glob("*.jpg"):
        asin = f.stem.replace("clean_focus_product_", "").replace("focus_product_", "").replace("_ai", "").replace("flux_", "")
        clean_files[asin] = f

print("==================================================")
print("🔍 HYPER-PRECISE IMAGE & ASIN AUDIT REPORT")
print("==================================================")
print(f"📌 Storefront Active Cards in index.html: {len(index_asins)}")
print(f"📌 Master Product Price Registry Items:  {len(registry)}")
print(f"📌 Global Direct Geo-Matrix Items:      {len(matrix)}")
print(f"📌 Raw Amazon Seller Images (raw_images/): {len(raw_files)}")
print(f"📌 Clean Flux Dev AI Images (flux_clean_images/): {len(clean_files)}")
print("==================================================")

mismatches = []
table_rows = []

for idx, asin in enumerate(index_asins, 1):
    reg_title = registry.get(asin, {}).get("title", f"Product {asin}")
    raw_f = raw_files.get(asin)
    clean_f = clean_files.get(asin)

    raw_status = "❌ MISSING"
    raw_dim = "N/A"
    if raw_f and raw_f.exists():
        try:
            with Image.open(raw_f) as img:
                raw_dim = f"{img.width}x{img.height} ({raw_f.stat().st_size // 1024}KB)"
                raw_status = f"✅ OK ({raw_f.name})"
        except Exception as e:
            raw_status = f"⚠️ CORRUPT ({e})"

    clean_status = "❌ MISSING"
    clean_dim = "N/A"
    if clean_f and clean_f.exists():
        try:
            with Image.open(clean_f) as img:
                clean_dim = f"{img.width}x{img.height} ({clean_f.stat().st_size // 1024}KB)"
                clean_status = f"✅ OK ({clean_f.name})"
        except Exception as e:
            clean_status = f"⚠️ CORRUPT ({e})"

    print(f"\n[{idx}/{len(index_asins)}] ASIN: {asin} - '{reg_title[:45]}'")
    print(f"  └─ Raw Image:   {raw_status} -> {raw_dim}")
    print(f"  └─ Clean Image: {clean_status} -> {clean_dim}")

    if "MISSING" in raw_status or "MISSING" in clean_status or "CORRUPT" in raw_status or "CORRUPT" in clean_status:
        mismatches.append(asin)

print("\n==================================================")
print("🔍 UNLINKED / EXTRA FILES CHECK")
print("==================================================")
extra_raw = set(raw_files.keys()) - set(index_asins)
extra_clean = set(clean_files.keys()) - set(index_asins)
print(f"Extra / Unlinked Raw Files: {list(extra_raw) if extra_raw else 'None (0)'}")
print(f"Extra / Unlinked Clean Files: {list(extra_clean) if extra_clean else 'None (0)'}")
print(f"Total Mismatches or Corrupt Images: {len(mismatches)}")
print("==================================================")
