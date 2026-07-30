import urllib.request
import re

candidates = [
    ("B08L7V89L6", "Floating Levitating Magnetic Plant Pot"),
    ("B09QGN9725", "Gold Ginkgo Leaf Metal Wall Art"),
    ("B0DZFGTCLR", "Flameless Top-Down Candle Warmer Lamp"),
    ("B093S4S6XG", "Golden Hour Sunset Projection Lamp")
]

tag = "smartdeal0358-21"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

for asin, label in candidates:
    url = f"https://www.amazon.com/dp/{asin}?tag={tag}"
    req = urllib.request.Request(url, headers=headers)
    try:
        res = urllib.request.urlopen(req, timeout=5)
        html = res.read().decode('utf-8', errors='ignore')
        title_m = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        title = title_m.group(1).replace('Amazon.com:', '').strip() if title_m else label
        print(f"[TEST RESULT] {asin} -> {title[:50]} | URL: {url}")
    except Exception as e:
        print(f"[TEST FAIL] {asin}: {e}")
