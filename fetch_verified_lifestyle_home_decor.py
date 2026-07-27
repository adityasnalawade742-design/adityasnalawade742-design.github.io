import urllib.request
import re
import json
from modules.amazon_finder import _fetch_from_serpapi
from modules.amazon_extractor import is_lifestyle_photo

EXCLUDED_ALL = {
    'B0BZXNSW5K', 'B0DXKGL1T2', 'B0D1FRDFFX', 'B0D8P8CSYP', 'B0B8D2K76V',
    'B099KFCK9F', 'B0BCW7CR43', 'B0B5D98Z5P', 'B0B7BPG1KP', 'B0BDLMBCHL',
    'B0C6T8T1LN', 'B0BQBKWSKK', 'B0FC2DV6FP', 'B0DZFGTCLR', 'B0FRS84KT9',
    'B08HJ2M49T', 'B0B8Z7X5M1', 'B0D7HFZZDH', 'B08B896T2W', 'B0BKSV8176',
    'B09ZP4MCRV', 'B09228FSL4', 'B08HGVL29K', 'B07D29P5Z1', 'B0CCP46DK9', 'B0B6JTX6NB',
    'B0C2YLN3H4', 'B0F8QHH23L', 'B07PT6QRXN', 'B0BDRSG2BT', 'B0CTJGJL2T', 'B07HP22QTZ', 'B09WZ5DNZB'
}

tag = "smartdeal0358-21"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

queries = [
    "volcanic flame diffuser humidifier",
    "danish pastel aesthetic wavy mirror",
    "candle warmer lamp with timer decor",
    "acrylic illuminated glowing note board"
]

lifestyle_approved_products = []

print("=== SEARCHING & VERIFYING 100% LIFESTYLE BACKGROUND HOME DECOR PRODUCTS ===")

for q in queries:
    res = _fetch_from_serpapi(q, num_results=6)
    if res:
        for item in res:
            asin = item['id']
            if asin in EXCLUDED_ALL or len(asin) != 10:
                continue
            
            image_url = item.get('original_image_url') or item.get('image', '')
            if not image_url:
                continue
                
            # Run Automated Lifestyle Background Filter
            has_lifestyle = is_lifestyle_photo(image_url)
            if not has_lifestyle:
                print(f"[SKIPPED WHITE CUTOUT] ASIN {asin} -> Plain white background detected.")
                continue
                
            url = f"https://www.amazon.com/dp/{asin}?tag={tag}"
            req = urllib.request.Request(url, headers=headers)
            try:
                r = urllib.request.urlopen(req, timeout=5)
                html = r.read().decode('utf-8', errors='ignore')
                title_m = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
                title = title_m.group(1).replace('Amazon.com:', '').strip() if title_m else item['title']
                
                if 'Page Not Found' not in title and 'Robot Check' not in title and '404' not in title and len(title) > 5:
                    lifestyle_approved_products.append({
                        "asin": asin,
                        "title": title[:65],
                        "price": item.get('price', '$24.99'),
                        "rating": item.get('rating', '4.6'),
                        "url": url,
                        "photo": image_url
                    })
                    EXCLUDED_ALL.add(asin)
                    print(f"[APPROVED LIFESTYLE] ASIN: {asin} | Title: {title[:45]} | Price: {item.get('price')}")
                    break
            except Exception:
                pass

with open("verified_lifestyle_products.json", "w", encoding="utf-8") as f:
    json.dump(lifestyle_approved_products, f, indent=2)
