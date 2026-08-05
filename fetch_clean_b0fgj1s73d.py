import sys
import urllib.request
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

url = "https://www.amazon.com/dp/B0FGJ1S73D"
req = urllib.request.Request(
    url,
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
)

html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
m = re.search(r'https://m\.media-amazon\.com/images/I/[A-Za-z0-9%_\-]+\.jpg', html)
if m:
    img_url = m.group(0)
    img_url = re.sub(r'\._[A-Z0-9_]+_\.', '._AC_SL1500_.', img_url)
    print(f"Downloading clean image: {img_url}")
    img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
    img_data = urllib.request.urlopen(img_req, timeout=10).read()
    Path('raw_images/raw_B0FGJ1S73D.jpg').write_bytes(img_data)
    print("✅ Successfully replaced raw_images/raw_B0FGJ1S73D.jpg with clean Amazon photo!")
else:
    print("⚠️ Could not find media image URL in HTML.")
