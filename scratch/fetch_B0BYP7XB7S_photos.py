import sys
import json
import urllib.request
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent
cand_dir = repo_dir / "scratch" / "B0BYP7XB7S_candidates"
cand_dir.mkdir(parents=True, exist_ok=True)

url = "https://www.amazon.com/dp/B0BYP7XB7S"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

req = urllib.request.Request(url, headers=headers)
try:
    html = urllib.request.urlopen(req, timeout=12).read().decode("utf-8", errors="ignore")
    # Search dynamic image JSON blocks
    matches = re.findall(r'https://m\.media-amazon\.com/images/I/[A-Za-z0-9%\-_]+\.jpg', html)
    unique_imgs = []
    for m in matches:
        if not any(x in m for x in ["icon", "sprite", "logo", "pixel"]):
            high_res = re.sub(r'\._[A-Z0-9_]+_\.', '._AC_SL1500_.', m)
            if high_res not in unique_imgs:
                unique_imgs.append(high_res)

    print(f"Found {len(unique_imgs)} candidate photos for B0BYP7XB7S:")
    for idx, img_url in enumerate(unique_imgs[:7], 1):
        try:
            r = urllib.request.Request(img_url, headers=headers)
            data = urllib.request.urlopen(r, timeout=10).read()
            out_file = cand_dir / f"option_{idx}.jpg"
            out_file.write_bytes(data)
            print(f"Option {idx}: Saved {out_file.name} ({len(data)/1024:.1f} KB) - {img_url}")
        except Exception as e:
            print(f"Option {idx}: Error downloading {img_url}: {e}")

except Exception as e:
    print(f"Error scraping B0BYP7XB7S: {e}")
