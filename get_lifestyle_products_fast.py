import urllib.request
import re
import json
from modules.amazon_extractor import is_lifestyle_photo

candidates = [
    ("B099KFCK9F", "Fire Flame Essential Oil Diffuser with Warm LED Glow", "https://m.media-amazon.com/images/I/71Wl12cZJNL._AC_SL1500_.jpg", "$22.99"),
    ("B0BCW7CR43", "Vintage Glass Mushroom Touch Desk Lamp", "https://m.media-amazon.com/images/I/71qCnqRyWHL._AC_SL1500_.jpg", "$29.99"),
    ("B0BDLMBCHL", "Dimmable Candle Warmer Lamp with Timer", "https://m.media-amazon.com/images/I/71j3G2gXBxL._AC_SL1500_.jpg", "$32.99"),
    ("B0B5D98Z5P", "Golden Hour Sunset Projection Lamp Light", "https://m.media-amazon.com/images/I/71zjJtLCl5L._AC_SL1500_.jpg", "$17.99")
]

tag = "smartdeal0358-21"
headers = {'User-Agent': 'Mozilla/5.0'}

verified_lifestyle = []

print("Testing 4 candidates with Automated Lifestyle Background Filter...")
for asin, label, photo_url, price in candidates:
    url = f"https://www.amazon.com/dp/{asin}?tag={tag}"
    req = urllib.request.Request(url, headers=headers)
    try:
        res = urllib.request.urlopen(req, timeout=5)
        html = res.read().decode('utf-8', errors='ignore')
        title_m = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        title = title_m.group(1).replace('Amazon.com:', '').strip() if title_m else label
        
        has_lifestyle = is_lifestyle_photo(photo_url)
        status = "PASSED (VERIFIED LIFESTYLE BACKGROUND)" if has_lifestyle else "FAILED (PLAIN WHITE CUTOUT)"
        
        if 'Page Not Found' not in title and '404' not in title:
            verified_lifestyle.append({
                "asin": asin,
                "title": title[:65],
                "price": price,
                "lifestyle_status": status,
                "url": url
            })
            print(f"[VERIFIED] {asin} -> {title[:45]} | Price: {price} | Status: {status}")
    except Exception as e:
        print(f"[ERROR] {asin}: {e}")

with open("lifestyle_fast_verified.json", "w", encoding="utf-8") as f:
    json.dump(verified_lifestyle, f, indent=2)
