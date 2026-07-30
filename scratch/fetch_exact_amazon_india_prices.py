import sys
import time
import requests
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

asins = [
    ("B0DZD1X83N", "Minimalist Wood Lamp"),
    ("B0GYDXHF4G", "Flame Aroma Diffuser"),
    ("B0FXLYXM32", "White Wavy Mirror"),
    ("B0C2YLN3H4", "Donut Vase Set"),
    ("B07HP22QTZ", "Crystal Suncatcher"),
    ("B0BZXNSW5K", "Fenmzee Touch Lamp"),
    ("B0DXKGL1T2", "Lily of Valley Lamp"),
    ("B0D1FRDFFX", "Mushroom Lamp"),
    ("B0D8P8CSYP", "Cute Bird Lamp")
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en;q=0.9"
}

print("==================================================")
print("🔍 SCRAPING EXACT AMAZON INDIA (amazon.in) PRICES")
print("==================================================")

for asin, name in asins:
    url_in = f"https://www.amazon.in/dp/{asin}"
    price_in = "Not Found / Out of Stock"
    try:
        res = requests.get(url_in, headers=headers, timeout=6)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            offscreen = soup.select_one(".a-price .a-offscreen")
            if offscreen and offscreen.text:
                price_in = offscreen.text.strip()
            if not price_in or price_in == "Not Found / Out of Stock":
                whole = soup.select_one("span.a-price-whole")
                if whole:
                    price_in = f"₹{whole.text.strip()}"
    except Exception as e:
        price_in = f"Error: {e}"

    print(f"[{asin}] {name:25s} -> amazon.in price: {price_in}")
