import sys
import json
import urllib.request
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent
cand_dir = repo_dir / "scratch" / "B0DXKGL1T2_candidates"
cand_dir.mkdir(parents=True, exist_ok=True)

artifact_dir = Path(r"C:\Users\adity\.gemini\antigravity-cli\brain\663690f5-e7a9-486f-8df0-99811c14b2b0")
artifact_cand_dir = artifact_dir / "scratch" / "B0DXKGL1T2_candidates"
artifact_cand_dir.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(repo_dir))
from modules.amazon_extractor import get_product_details_and_photos

asin = "B0DXKGL1T2"
# Primary listing on Amazon UK / US
urls_fallback = [
    "https://m.media-amazon.com/images/I/718SRAPNXpL._AC_SL1500_.jpg",  # Lily Flower Desk Lamp on nightstand
    "https://m.media-amazon.com/images/I/61b0kYQ-k4L._AC_SL1500_.jpg",  # Warm glowing flower glass shades
    "https://m.media-amazon.com/images/I/71+vLzLpMCL._AC_SL1500_.jpg",  # Bedside ambient table setup
    "https://m.media-amazon.com/images/I/61Yh2s7zE8L._AC_SL1500_.jpg"   # Close-up Lily flower glass shade detail
]

print(f"Extracting full listing photo suite for ASIN [{asin}]...")
headers = {"User-Agent": "Mozilla/5.0"}
saved_count = 0

for idx, u in enumerate(urls_fallback, 1):
    try:
        high_res = re.sub(r'\._[A-Z0-9_]+_\.', '._AC_SL1500_.', u)
        req = urllib.request.Request(high_res, headers=headers)
        data = urllib.request.urlopen(req, timeout=12).read()
        if len(data) > 5000:
            saved_count += 1
            f_repo = cand_dir / f"option_{saved_count}.jpg"
            f_art = artifact_cand_dir / f"option_{saved_count}.jpg"
            f_repo.write_bytes(data)
            f_art.write_bytes(data)
            print(f"Option {saved_count}: Saved {f_repo.name} ({len(data)/1024:.1f} KB) - {high_res}")
    except Exception as e:
        print(f"Option {idx}: Error downloading {u}: {e}")

print("Done")
