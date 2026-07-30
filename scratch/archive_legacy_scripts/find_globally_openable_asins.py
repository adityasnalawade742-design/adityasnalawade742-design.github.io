import urllib.request
import urllib.parse
import re

# Test candidate ASINs for global 100% open rate without regional 404 redirect
test_asins = [
    ("B0B8D2K76V", "Minimalist Wood Lamp (Verified Working)"),
    ("B0BKSV8176", "Ceramic Donut Flower Vases"),
    ("B07D29P5Z1", "Glass Hydroponic Terrarium Planter"),
    ("B0CCP46DK9", "House Gem Electric Smart Mug Warmer"),
    ("B0B6JTX6NB", "Nextmug Temperature Self-Heating Mug"),
    ("B0B8Z7X5M1", "Minimalist Asymmetric Wavy Mirror"),
    ("B093S4S6XG", "Sunset Lamp Projection Light"),
    ("B0BKSV8176", "Nordic Ceramic Flower Vases")
]

tag = "smartdeal0358-21"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

print("Testing candidates for 100% global openability...")
openable_items = []

for asin, label in test_asins:
    url = f"https://www.amazon.com/dp/{asin}?tag={tag}"
    req = urllib.request.Request(url, headers=headers)
    try:
        res = urllib.request.urlopen(req, timeout=5)
        final_url = res.geturl()
        html = res.read().decode('utf-8', errors='ignore')
        
        # Check title and price
        title_m = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        title = title_m.group(1).replace('Amazon.com:', '').strip() if title_m else label
        
        if 'Page Not Found' not in title and 'Robot Check' not in title and '404' not in title and len(title) > 5:
            openable_items.append({
                "asin": asin,
                "title": title[:60],
                "url": f"https://www.amazon.com/dp/{asin}?tag={tag}"
            })
            print(f"[OPEN 100%] {asin} -> {title[:45]} | URL: https://www.amazon.com/dp/{asin}?tag={tag}")
    except Exception as e:
        print(f"[FAIL] {asin}: {e}")

print(f"\nTotal 100% openable items found: {len(openable_items)}")
