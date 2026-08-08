import sys
import json
import urllib.request
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_dir))

cand_dir = repo_dir / "scratch" / "B0DXKGL1T2_true_candidates"
cand_dir.mkdir(parents=True, exist_ok=True)

artifact_dir = Path(r"C:\Users\adity\.gemini\antigravity-cli\brain\663690f5-e7a9-486f-8df0-99811c14b2b0")
artifact_cand_dir = artifact_dir / "scratch" / "B0DXKGL1T2_true_candidates"
artifact_cand_dir.mkdir(parents=True, exist_ok=True)

from modules.amazon_finder import fetch_amazon_products
prods = fetch_amazon_products("Lily of the Valley Flower Table Lamp", num_results=5)

print(f"Retrieved {len(prods)} products for query:")
headers = {"User-Agent": "Mozilla/5.0"}
saved_count = 0

for p in prods:
    print(" -> Title:", p.get("title"))
    img_url = p.get("original_image_url") or p.get("image")
    if img_url and img_url.startswith("http"):
        try:
            high_res = re.sub(r'\._[A-Z0-9_]+_\.', '._AC_SL1500_.', img_url)
            req = urllib.request.Request(high_res, headers=headers)
            data = urllib.request.urlopen(req, timeout=12).read()
            if len(data) > 5000:
                saved_count += 1
                f_repo = cand_dir / f"true_option_{saved_count}.jpg"
                f_art = artifact_cand_dir / f"true_option_{saved_count}.jpg"
                f_repo.write_bytes(data)
                f_art.write_bytes(data)
                print(f"  Option {saved_count}: Saved {f_repo.name} ({len(data)/1024:.1f} KB) - {high_res}")
        except Exception as e:
            print(f"  Error downloading {img_url}: {e}")

print("Done")
