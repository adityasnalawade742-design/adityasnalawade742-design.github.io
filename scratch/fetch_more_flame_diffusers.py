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

# Authentic Flame Mist Diffuser Photos from Amazon
urls = [
    "https://m.media-amazon.com/images/I/71+SDMHPVGL._AC_SL1500_.jpg",  # Black Flame Air Diffuser with Fire Mist Effect
    "https://m.media-amazon.com/images/I/61l+6V61bBL._AC_SL1500_.jpg",  # Ultrasonic Aroma Flame Diffuser Bedroom Glow
    "https://m.media-amazon.com/images/I/71V36z73yAL._AC_SL1500_.jpg"   # Volcano Crackle Flame Diffuser
]

headers = {"User-Agent": "Mozilla/5.0"}

print("Downloading authentic Flame Aroma Diffuser listing photos...")
for idx, u in enumerate(urls, 1):
    try:
        req = urllib.request.Request(u, headers=headers)
        data = urllib.request.urlopen(req, timeout=12).read()
        f_repo = cand_dir / f"option_{idx}.jpg"
        f_art = artifact_cand_dir / f"option_{idx}.jpg"
        f_repo.write_bytes(data)
        f_art.write_bytes(data)
        print(f"Option {idx}: Saved {f_repo.name} ({len(data)/1024:.1f} KB)")
    except Exception as e:
        print(f"Option {idx}: Error downloading {u}: {e}")

print("Done")
