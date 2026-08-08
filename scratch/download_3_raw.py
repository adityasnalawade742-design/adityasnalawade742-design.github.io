import sys, json, re, urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent
raw_dir = repo_dir / "raw_images"

urls = {
    "B0GYDXHF4G": "https://www.amazon.ca/dp/B0GYDXHF4G",
    "B07HP22QTZ": "https://www.amazon.co.uk/dp/B07HP22QTZ",
    "B0DXKGL1T2": "https://www.amazon.co.uk/dp/B0DXKGL1T2"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5"
}

for asin, url in urls.items():
    print(f"Fetching {asin} from {url}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
        matches = re.findall(r'https://m\.media-amazon\.com/images/I/[A-Za-z0-9%\-_]+\.jpg', html)
        valid = [m for m in matches if "SL1500" in m or "_AC_SY" in m or "_AC_SX" in m or "_AC_UL" in m]
        if not valid:
            valid = [m for m in matches if not any(x in m for x in ["icon", "sprite", "logo", "pixel"])]
        if valid:
            img_url = re.sub(r'\._[A-Z0-9_]+_\.', '._AC_SL1500_.', valid[0])
            print(f" -> Found image: {img_url}")
            img_data = urllib.request.urlopen(urllib.request.Request(img_url, headers=headers), timeout=10).read()
            (raw_dir / f"raw_{asin}.jpg").write_bytes(img_data)
            print(f" ✅ Saved raw_{asin}.jpg successfully!")
        else:
            print(f" ⚠️ No valid image matched for {asin}")
    except Exception as e:
        print(f" ⚠️ Exception for {asin}: {e}")

