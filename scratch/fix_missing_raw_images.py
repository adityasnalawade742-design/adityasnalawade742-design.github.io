import sys
import shutil
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent
raw_dir = repo_dir / "raw_images"
raw_dir.mkdir(exist_ok=True)

by_src = repo_dir / "scratch" / "B0BYP7XB7S_candidates" / "option_4.jpg"
by_dst = raw_dir / "raw_B0BYP7XB7S.jpg"
if by_src.exists():
    shutil.copy(by_src, by_dst)
    print(f"✅ Restored {by_dst.name} ({by_dst.stat().st_size // 1024} KB)")

c2_src = repo_dir / "scratch" / "B0C2YLN3H4_candidates" / "option_6.jpg"
c2_dst = raw_dir / "raw_B0C2YLN3H4.jpg"
if c2_src.exists():
    shutil.copy(c2_src, c2_dst)
    print(f"✅ Restored {c2_dst.name} ({c2_dst.stat().st_size // 1024} KB)")

raw_files = list(raw_dir.glob("*.jpg"))
print(f"==================================================")
print(f"FINAL RAW IMAGES COUNT: {len(raw_files)} / 21")
print(f"==================================================")
