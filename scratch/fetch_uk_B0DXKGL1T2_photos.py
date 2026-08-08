import sys
import json
import urllib.request
import re
from pathlib import Path
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent
cand_dir = repo_dir / "scratch" / "B0DXKGL1T2_candidates"
cand_dir.mkdir(parents=True, exist_ok=True)

artifact_dir = Path(r"C:\Users\adity\.gemini\antigravity-cli\brain\663690f5-e7a9-486f-8df0-99811c14b2b0")
artifact_cand_dir = artifact_dir / "scratch" / "B0DXKGL1T2_candidates"
artifact_cand_dir.mkdir(parents=True, exist_ok=True)

url = "https://www.amazon.co.uk/dp/B0DXKGL1T2"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en;q=0.9"
}

print("Scraping Amazon UK for Lily of the Valley Flower Desk Lamp (B0DXKGL1T2)...")
try:
    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req, timeout=12).read().decode("utf-8", errors="ignore")
    matches = re.findall(r'https://m\.media-amazon\.com/images/I/[A-Za-z0-9%\-_]+\.jpg', html)
    unique_imgs = []
    for m in matches:
        if not any(x in m for x in ["icon", "sprite", "logo", "pixel"]):
            high_res = re.sub(r'\._[A-Z0-9_]+_\.', '._AC_SL1500_.', m)
            if high_res not in unique_imgs:
                unique_imgs.append(high_res)

    print(f"Retrieved {len(unique_imgs)} photos from Amazon UK:")
    saved_count = 0
    for idx, img_url in enumerate(unique_imgs, 1):
        try:
            r = urllib.request.Request(img_url, headers=headers)
            data = urllib.request.urlopen(r, timeout=10).read()
            if len(data) > 10000:
                saved_count += 1
                out_file = cand_dir / f"option_{saved_count}.jpg"
                out_art = artifact_cand_dir / f"option_{saved_count}.jpg"
                out_file.write_bytes(data)
                out_art.write_bytes(data)
                print(f"Option {saved_count}: Saved {out_file.name} ({len(data)/1024:.1f} KB) - {img_url}")
                if saved_count >= 6:
                    break
        except Exception as e:
            print(f"Option {idx}: Error {e}")

except Exception as e:
    print(f"Error scraping UK photos: {e}")
