import sys
import urllib.request
import re
import shutil
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent
cand_dir = repo_dir / "scratch" / "B0BPM41R5C_candidates"
cand_dir.mkdir(parents=True, exist_ok=True)

artifact_dir = Path(r"C:\Users\adity\.gemini\antigravity-cli\brain\663690f5-e7a9-486f-8df0-99811c14b2b0")
artifact_cand_dir = artifact_dir / "scratch" / "B0BPM41R5C_candidates"
artifact_cand_dir.mkdir(parents=True, exist_ok=True)

urls = [
    "https://m.media-amazon.com/images/I/61-+Q3U-gPL._AC_SL1500_.jpg",  # Ceramic Hand Sculpture Ring Holder setup
    "https://m.media-amazon.com/images/I/71p0W1e-JLL._AC_SL1500_.jpg",  # Side view jewelry tray setup
    "https://m.media-amazon.com/images/I/71pU8b3mJ+L._AC_SL1500_.jpg",  # Vanity table setup with rings & bracelets
    "https://m.media-amazon.com/images/I/61N+V+K5RJL._AC_SL1500_.jpg"   # Close up ceramic hand texture detail
]

headers = {"User-Agent": "Mozilla/5.0"}

print("Downloading fallback candidate photos for B0BPM41R5C...")
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
