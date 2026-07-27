import urllib.request
import re
import json
from modules.amazon_extractor import is_lifestyle_photo, is_adult_aesthetic_product

candidates = [
    ("B0C4FTJ1CN", "Volcanic Erupting Flame Essential Oil Diffuser", "https://m.media-amazon.com/images/I/71Wl12cZJNL._AC_SL1500_.jpg", "$27.99"),
    ("B0FXLYXM32", "Pocetry 22x30 Inch White Wavy Vanity Wall Mirror", "https://m.media-amazon.com/images/I/61SsDfH706L._AC_SL1500_.jpg", "$24.99"),
    ("B0FRLWC6X9", "Flameless Top-Down Candle Warmer Lamp with Timer", "https://m.media-amazon.com/images/I/71j3G2gXBxL._AC_SL1500_.jpg", "$13.99"),
    ("B07PT6QRXN", "Mkono 2-Pack Boho Macrame Woven Wall Hanging Decor", "https://m.media-amazon.com/images/I/71qCnqRyWHL._AC_SL1500_.jpg", "$19.99")
]

tag = "smartdeal0358-21"
headers = {'User-Agent': 'Mozilla/5.0'}

verified = []

print("=== VERIFYING ADULT ELEGANT HOME DECOR PRODUCTS ===")
for asin, label, photo_url, price in candidates:
    if not is_adult_aesthetic_product(label):
        print(f"[REJECTED KIDS ITEM] {asin} -> '{label}'")
        continue
    url = f"https://www.amazon.com/dp/{asin}?tag={tag}"
    req = urllib.request.Request(url, headers=headers)
    try:
        res = urllib.request.urlopen(req, timeout=5)
        html = res.read().decode('utf-8', errors='ignore')
        title_m = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        title = title_m.group(1).replace('Amazon.com:', '').strip() if title_m else label
        
        has_lifestyle = is_lifestyle_photo(photo_url)
        
        if 'Page Not Found' not in title and '404' not in title:
            verified.append({
                "asin": asin,
                "title": title[:65],
                "price": price,
                "url": url
            })
            print(f"[VERIFIED ADULT DECOR] {asin} -> {title[:45]} | Price: {price}")
    except Exception as e:
        print(f"[ERROR] {asin}: {e}")

with open("adult_decor_fast_verified.json", "w", encoding="utf-8") as f:
    json.dump(verified, f, indent=2)
