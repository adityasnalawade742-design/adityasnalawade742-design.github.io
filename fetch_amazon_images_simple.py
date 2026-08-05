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
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

print(f"🌐 Fetching Amazon product images for [{asin}]...")

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        
    matches = re.findall(r'https://m\.media-amazon\.com/images/I/[A-Za-z0-9_\-%\.]+\.jpg', html)
    
    unique_urls = []
    seen = set()
    for m in matches:
        # Get clean high-res URL
        clean_url = re.sub(r'\._[A-Z0-9_,]+_\.', '.', m)
        if clean_url not in seen and 'sprite' not in clean_url and 'icon' not in clean_url and 'logo' not in clean_url:
            seen.add(clean_url)
            unique_urls.append(clean_url)
            
    print(f"📷 Found {len(unique_urls)} candidate image URLs!")

    for idx, img_url in enumerate(unique_urls[:5], 1):
        save_path = output_dir / f"candidate_{idx}.jpg"
        try:
            r = urllib.request.Request(img_url, headers={'User-Agent': headers['User-Agent']})
            with urllib.request.urlopen(r) as response, open(save_path, 'wb') as out_f:
                out_f.write(response.read())
            print(f"  • Candidate {idx}: {save_path.name} | URL: {img_url}")
        except Exception as e_dl:
            print(f"  ⚠️ Error candidate {idx}: {e_dl}")

except Exception as e:
    print(f"❌ Error: {e}")
