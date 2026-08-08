import sys, json, re, urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent
raw_dir = repo_dir / "raw_images"

cache_path = repo_dir / "serpapi_cache.json"
if cache_path.exists():
    content = cache_path.read_text(encoding="utf-8")
    for asin in ['B0GYDXHF4G', 'B07HP22QTZ', 'B0DXKGL1T2']:
        m = re.findall(rf'https://m\.media-amazon\.com/images/I/[^"\']+\.jpg', content)
        print(f"ASIN {asin} media images found in cache: {len(m)}")

print("Done")
