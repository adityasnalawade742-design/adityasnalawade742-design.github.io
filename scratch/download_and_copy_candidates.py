import sys
import json
import urllib.request
import shutil
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent
cand_dir = repo_dir / "scratch" / "B0BYP7XB7S_candidates"
cand_dir.mkdir(parents=True, exist_ok=True)

artifact_dir = Path(r"C:\Users\adity\.gemini\antigravity-cli\brain\663690f5-e7a9-486f-8df0-99811c14b2b0")
artifact_cand_dir = artifact_dir / "scratch" / "B0BYP7XB7S_candidates"
artifact_cand_dir.mkdir(parents=True, exist_ok=True)

urls = [
    "https://m.media-amazon.com/images/I/61--H3UWSfL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/71hLftTxxZL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/71smSRbKWnL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/71k74vcuhjL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/71ZrE2DUaPL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/61WJB1lW2ML._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/71gg5OOK4HL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/71HXPMnUERL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/61Vwz0E+5tL._AC_SL1500_.jpg"
]

headers = {"User-Agent": "Mozilla/5.0"}

print("Downloading 9 candidate listing photos for B0BYP7XB7S...")
for idx, u in enumerate(urls, 1):
    try:
        req = urllib.request.Request(u, headers=headers)
        data = urllib.request.urlopen(req, timeout=12).read()
        f_repo = cand_dir / f"option_{idx}.jpg"
        f_artifact = artifact_cand_dir / f"option_{idx}.jpg"
        f_repo.write_bytes(data)
        f_artifact.write_bytes(data)
        print(f"Option {idx}: Saved {f_repo.name} ({len(data)/1024:.1f} KB)")
    except Exception as e:
        print(f"Option {idx}: Error {e}")

print("All candidate photos saved!")
