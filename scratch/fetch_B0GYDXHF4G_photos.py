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

urls = [
    "https://m.media-amazon.com/images/I/71V36z73yAL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/71-0+6y2Q0L._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/71oWqnkgf9L._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/71uarLUS-jL._AC_SL1500_.jpg"
]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

print("Downloading candidate listing photos for Flame Aroma Diffuser (B0GYDXHF4G)...")
downloaded = []
for idx, u in enumerate(urls, 1):
    try:
        req = urllib.request.Request(u, headers=headers)
        data = urllib.request.urlopen(req, timeout=12).read()
        f_repo = cand_dir / f"option_{idx}.jpg"
        f_art = artifact_cand_dir / f"option_{idx}.jpg"
        f_repo.write_bytes(data)
        f_art.write_bytes(data)
        downloaded.append((idx, u, len(data)))
        print(f"Option {idx}: Saved {f_repo.name} ({len(data)/1024:.1f} KB)")
    except Exception as e:
        print(f"Option {idx}: Error downloading {u}: {e}")

# Save raw_B0GYDXHF4G.jpg default as option 1
if downloaded:
    raw_target = repo_dir / "raw_images" / "raw_B0GYDXHF4G.jpg"
    raw_target.parent.mkdir(exist_ok=True)
    raw_target.write_bytes((cand_dir / "option_1.jpg").read_bytes())
    print(f"✅ Saved raw_images/raw_B0GYDXHF4G.jpg default from Option 1")

