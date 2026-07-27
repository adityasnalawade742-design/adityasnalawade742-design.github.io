import urllib.request
import re

# Test candidate Amazon ASINs for 100% live product status
test_asins = [
    'B0BZXNSW5K', # Worked!
    'B09ZP4MCRV', # Touch Lamp
    'B0B5D98Z5P', # Sunset Lamp
    'B09LVBFT4H', # Flame Diffuser
    'B09YHCSYRT', # Acrylic LED Board
    'B0B8C862N9', # Mushroom Lamp
    'B0BS3L71R4', # Candle Warmer
    'B09228FSL4'  # Sunset Projector
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

print("Checking active live Amazon ASINs:")
for a in test_asins:
    url = f"https://www.amazon.com/dp/{a}"
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=6).read().decode('utf-8', errors='ignore')
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        title = title_match.group(1).replace('Amazon.com:', '').strip() if title_match else 'No Title'
        if 'Page Not Found' not in title and 'Robot Check' not in title and '404' not in title:
            print(f"[LIVE CONFIRMED] ASIN {a} -> {title[:50]} | URL: {url}")
        else:
            print(f"[FAILED 404] ASIN {a} -> {title[:30]}")
    except Exception as e:
        print(f"[ERROR] ASIN {a}: {e}")
