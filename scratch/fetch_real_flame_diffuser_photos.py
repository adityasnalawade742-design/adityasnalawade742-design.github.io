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

# Genuine Aegci Flame Air Diffuser Humidifier listing photos
urls = [
    "https://m.media-amazon.com/images/I/71+SDMHPVGL._AC_SL1500_.jpg",  # Black Flame Diffuser with Fire Mist
    "https://m.media-amazon.com/images/I/61+t-y61LSL._AC_SL1500_.jpg",  # Warm Orange LED Fireplace Effect
    "https://m.media-amazon.com/images/I/71V36z73yAL._AC_SL1500_.jpg",  # Dark Crackle Flame Humidifier
    "https://m.media-amazon.com/images/I/71-0+6y2Q0L._AC_SL1500_.jpg"   # Bedside Aromatherapy Glow
]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

print("Downloading authentic Flame Aroma Diffuser listing photos...")
saved = []
for idx, u in enumerate(urls, 1):
    try:
        req = urllib.request.Request(u, headers=headers)
        data = urllib.request.urlopen(req, timeout=12).read()
        f_repo = cand_dir / f"option_{idx}.jpg"
        f_art = artifact_cand_dir / f"option_{idx}.jpg"
        f_repo.write_bytes(data)
        f_art.write_bytes(data)
        saved.append(idx)
        print(f"Option {idx}: Saved {f_repo.name} ({len(data)/1024:.1f} KB) - {u}")
    except Exception as e:
        print(f"Option {idx}: Error {e}")

print("Done")
