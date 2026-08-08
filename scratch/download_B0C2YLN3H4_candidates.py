import sys
import urllib.request
import re
import shutil
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent
cand_dir = repo_dir / "scratch" / "B0C2YLN3H4_candidates"
cand_dir.mkdir(parents=True, exist_ok=True)

artifact_dir = Path(r"C:\Users\adity\.gemini\antigravity-cli\brain\663690f5-e7a9-486f-8df0-99811c14b2b0")
artifact_cand_dir = artifact_dir / "scratch" / "B0C2YLN3H4_candidates"
artifact_cand_dir.mkdir(parents=True, exist_ok=True)

urls = [
    "https://m.media-amazon.com/images/I/71+K2WB572L._AC_SL1500_.jpg",  # Option 1: White Donut Vases Set with Pampas Grass
    "https://m.media-amazon.com/images/I/71ss7oYHwBL._AC_SL1500_.jpg",  # Option 2: Side-by-side Matte Donut Vases
    "https://m.media-amazon.com/images/I/71GJizcoJCL._AC_SL1500_.jpg",  # Option 3: Modern Living Room Coffee Table Setup
    "https://m.media-amazon.com/images/I/71-NdgWxkFL._AC_SL1500_.jpg"   # Option 4: Close-up Ceramic Texture & Grain
]

headers = {"User-Agent": "Mozilla/5.0"}

print("Downloading candidate photos for B0C2YLN3H4...")
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
        print(f"Option {idx}: Error {e}")

print("Done")
