import re
import urllib.request
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path(__file__).resolve().parent
output_dir = repo / "b07hp22qtz_candidates"
output_dir.mkdir(exist_ok=True)

asin = "B07HP22QTZ"
url = f"https://www.amazon.com/dp/{asin}"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

raw_urls = re.findall(r'https://m\.media-amazon\.com/images/I/([^"\'\s>\)]+)', html)

distinct_urls = []
seen = set()
for url_part in raw_urls:
    # Extract base image ID before parameters like ._AC_...
    base_id = url_part.split('.')[0]
    if len(base_id) >= 8 and base_id not in seen and not any(x in base_id.lower() for x in ['sprite', 'icon', 'logo', 'play', 'badge']):
        seen.add(base_id)
        full_url = f"https://m.media-amazon.com/images/I/{base_id}.jpg"
        distinct_urls.append(full_url)

print(f"📷 Found {len(distinct_urls)} distinct high-res product photo IDs!")

candidates = []
for idx, img_url in enumerate(distinct_urls[:6], 1):
    save_path = output_dir / f"candidate_{idx}.jpg"
    try:
        r = urllib.request.Request(img_url, headers=headers)
        with urllib.request.urlopen(r) as response, open(save_path, 'wb') as out_f:
            out_f.write(response.read())
        candidates.append((idx, img_url, str(save_path)))
        print(f"  • Option {idx}: {img_url}")
    except Exception as e:
        print(f"  ⚠️ Error Option {idx}: {e}")
