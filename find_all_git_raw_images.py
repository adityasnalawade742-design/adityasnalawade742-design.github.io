import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Get list of all commits
res = subprocess.run(["git", "log", "--format=%H %s"], capture_output=True, text=True, encoding="utf-8")
commits = [line.split(maxsplit=1) for line in res.stdout.strip().split("\n") if line]

print("🔍 SEARCHING ALL COMMITS FOR CLEAN FLUX DEV RAW IMAGES...")
print("=" * 80)

found_map = {}

for commit_hash, commit_msg in commits:
    tree_res = subprocess.run(["git", "ls-tree", "-r", "--name-only", commit_hash], capture_output=True, text=True, encoding="utf-8")
    files = tree_res.stdout.splitlines()
    for f in files:
        if ("raw_" in f or "focus_" in f or "generated" in f or "scratch" in f or "test_" in f) and f.endswith((".jpg", ".png", ".webp")):
            if f not in found_map:
                found_map[f] = (commit_hash[:7], commit_msg[:40])

for path, (chash, cmsg) in sorted(found_map.items()):
    print(f"  • {path:<40} | Commit: {chash} ({cmsg})")

print("=" * 80)
