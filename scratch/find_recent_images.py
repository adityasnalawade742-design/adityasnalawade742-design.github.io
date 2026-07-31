import sys
import os
from pathlib import Path
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")

image_files = []
for p in repo.glob("**/*"):
    if p.is_file() and p.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
        # Exclude .git and __pycache__
        if ".git" not in str(p) and "__pycache__" not in str(p):
            mtime = os.path.getmtime(p)
            image_files.append((mtime, p))

image_files.sort(key=lambda x: x[0], reverse=True)

print("==================================================")
print("🖼️ ALL RECENT IMAGE FILES IN REPOSITORY (NEWEST FIRST)")
print("==================================================")

for mtime, path in image_files[:20]:
    dt = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    rel = path.relative_to(repo)
    print(f" • {dt} | {path.stat().st_size:9d} bytes | {str(rel)}")
