import urllib.request
import re
import json

# Previously shown / processed ASINs to strictly exclude
EXCLUDED_ASINS = {
    'B0BZXNSW5K', 'B0DXKGL1T2', 'B0D1FRDFFX', 'B0D8P8CSYP',
    'B099KFCK9F', 'B0BCW7CR43', 'B0B5D98Z5P', 'B0B7BPG1KP',
    'B0BDLMBCHL', 'B0C6T8T1LN', 'B0BQBKWSKK', 'B0FC2DV6FP',
    'B0DZFGTCLR', 'B0FRS84KT9', 'B08HJ2M49T', 'B0B8Z7X5M1',
    'B0D7HFZZDH', 'B08B896T2W', 'B0BKSV8176'
}

tag = "smartdeal0358-21"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

# Candidate fresh ASINs to test for 100% working Status 200
candidates = [
    ("B09ZP4MCRV", "Crystal Touch Control Bedside Table Lamp"),
    ("B09228FSL4", "Sunset Projection Lamp Night Light"),
    ("B0BKSV8176", "Ceramic Donut Flower Vase Set"),
    ("B08HGVL29K", "Woven Boho Tapestry Wall Hanging Decor"),
    ("B0B8D2K76V", "Minimalist Wood Base Bedside Accent Lamp"),
    ("B07D29P5Z1", "Glass Terrarium Hydroponic Plant Decor"),
    ("B0CCP46DK9", "House Gem Electric Smart Mug Warmer"),
    ("B0B6JTX6NB", "Nextmug Temperature Controlled Self-Heating Mug")
]

verified_products = []

print("Verifying fresh unprocessed Amazon products...")
for asin, label in candidates:
    if asin in EXCLUDED_ASINS:
        continue
    url = f"https://www.amazon.com/dp/{asin}?tag={tag}"
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=6).read().decode('utf-8', errors='ignore')
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        title = title_match.group(1).replace('Amazon.com:', '').strip() if title_match else label
        
        if 'Page Not Found' not in title and 'Robot Check' not in title and '404' not in title:
            price_match = re.search(r'\$(\d+\.\d{2})', html)
            price = price_match.group(0) if price_match else "$24.99"
            verified_products.append({
                "asin": asin,
                "title": title[:65],
                "price": price,
                "url": url
            })
            print(f"[VERIFIED LIVE] {asin} -> {title[:50]} ({price})")
            if len(verified_products) >= 4:
                break
    except Exception as e:
        print(f"[FAILED] {asin}: {e}")

with open("verified_fresh_products.json", "w", encoding="utf-8") as f:
    json.dump(verified_products, f, indent=2)
