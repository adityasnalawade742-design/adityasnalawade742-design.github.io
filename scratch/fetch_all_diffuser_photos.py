import sys
import json
import urllib.request
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent
cand_dir = repo_dir / "scratch" / "B0GYDXHF4G_candidates"
cand_dir.mkdir(parents=True, exist_ok=True)

artifact_dir = Path(r"C:\Users\adity\.gemini\antigravity-cli\brain\663690f5-e7a9-486f-8df0-99811c14b2b0")
artifact_cand_dir = artifact_dir / "scratch" / "B0GYDXHF4G_candidates"
artifact_cand_dir.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(repo_dir))
from modules.amazon_extractor import get_product_details_and_photos
prod = get_product_details_and_photos("https://www.amazon.com/dp/B0GYDXHF4G")
photos = prod.get("all_photos", [])

print(f"Extracted {len(photos)} photos for B0GYDXHF4G:")
headers = {"User-Agent": "Mozilla/5.0"}

for idx, u in enumerate(photos[:8], 1):
    try:
        high_res = re.sub(r'\._[A-Z0-9_]+_\.', '._AC_SL1500_.', u)
        req = urllib.request.Request(high_res, headers=headers)
        data = urllib.request.urlopen(req, timeout=12).read()
        f_repo = cand_dir / f"option_{idx}.jpg"
        f_art = artifact_cand_dir / f"option_{idx}.jpg"
        f_repo.write_bytes(data)
        f_art.write_bytes(data)
        print(f"Option {idx}: Saved {f_repo.name} ({len(data)/1024:.1f} KB) - {high_res}")
    except Exception as e:
        print(f"Option {idx}: Error {e}")

