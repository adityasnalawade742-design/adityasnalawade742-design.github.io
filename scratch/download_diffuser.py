import urllib.request, re
from pathlib import Path

url = "https://www.amazon.com/dp/B0GYDXHF4G"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

try:
    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
    matches = re.findall(r'https://m\.media-amazon\.com/images/I/[A-Za-z0-9%\-_]+\.jpg', html)
    valid = [m for m in matches if not any(x in m for x in ["icon", "sprite", "logo", "pixel"])]
    if valid:
        img_url = re.sub(r'\._[A-Z0-9_]+_\.', '._AC_SL1500_.', valid[0])
        print("Found B0GYDXHF4G image:", img_url)
        img_data = urllib.request.urlopen(urllib.request.Request(img_url, headers=headers), timeout=10).read()
        Path("raw_images/raw_B0GYDXHF4G.jpg").write_bytes(img_data)
        print("Saved raw_B0GYDXHF4G.jpg successfully!")
    else:
        print("No matches found for B0GYDXHF4G")
except Exception as e:
    print("Error:", e)
