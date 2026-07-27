import urllib.request
import re
import json

# Strict list of all ASINs ever used/tested in this repo to exclude
EXCLUDED_ALL = {
    'B0BZXNSW5K', 'B0DXKGL1T2', 'B0D1FRDFFX', 'B0D8P8CSYP', 'B0B8D2K76V',
    'B099KFCK9F', 'B0BCW7CR43', 'B0B5D98Z5P', 'B0B7BPG1KP', 'B0BDLMBCHL',
    'B0C6T8T1LN', 'B0BQBKWSKK', 'B0FC2DV6FP', 'B0DZFGTCLR', 'B0FRS84KT9',
    'B08HJ2M49T', 'B0B8Z7X5M1', 'B0D7HFZZDH', 'B08B896T2W', 'B0BKSV8176',
    'B09ZP4MCRV', 'B09228FSL4', 'B08HGVL29K', 'B07D29P5Z1', 'B0CCP46DK9', 'B0B6JTX6NB'
}

tag = "smartdeal0358-21"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

# New candidates for Home Decor
candidates = [
    ("B09QGN9725", "Gold Metal Ginkgo Leaf Wall Sculpture Art Decor"),
    ("B0C77J2K1W", "Decorative Ceramic Bookend Set for Bookshelves"),
    ("B09T3NVK8B", "Vintage Amber Glass Bud Vase Set of 6"),
    ("B0BFLV5R9H", "Nordic Woven Cotton Macrame Plant Hanger Basket"),
    ("B09MKG2T8R", "Modern Geometric Ceramic Tissue Box Cover"),
    ("B0BP28J4G9", "Minimalist Arch Decorative Tray for Nightstand")
]

new_openable = []

print("Searching for brand new 100% openable Home Decor ASINs...")
for asin, label in candidates:
    if asin in EXCLUDED_ALL:
        continue
    url = f"https://www.amazon.com/dp/{asin}?tag={tag}"
    req = urllib.request.Request(url, headers=headers)
    try:
        res = urllib.request.urlopen(req, timeout=5)
        html = res.read().decode('utf-8', errors='ignore')
        title_m = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        title = title_m.group(1).replace('Amazon.com:', '').strip() if title_m else label
        
        if 'Page Not Found' not in title and 'Robot Check' not in title and '404' not in title and len(title) > 5:
            new_openable.append({
                "asin": asin,
                "title": title[:65],
                "url": url
            })
            print(f"[NEW OPEN 100%] {asin} -> {title[:45]} | URL: {url}")
            if len(new_openable) >= 4:
                break
    except Exception as e:
        print(f"[FAIL] {asin}: {e}")

with open("brand_new_products.json", "w", encoding="utf-8") as f:
    json.dump(new_openable, f, indent=2)
