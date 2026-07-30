import sys
import io
import json
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from modules.amazon_extractor import is_lifestyle_photo

candidates = [
    {
        "asin": "B0GT5GWK4B",
        "title": "Dreamholder Top-Down Candle Warmer Lamp with Timer",
        "price": "$14.99",
        "rating": "4.7★",
        "photo": "https://m.media-amazon.com/images/I/718y6K9B+JL._AC_SL1500_.jpg",
        "url": "https://www.amazon.com/dp/B0GT5GWK4B?tag=smartdeal0358-21"
    },
    {
        "asin": "B0C4FTJ1CN",
        "title": "YALEDI Volcano Flame Essential Oil Aroma Diffuser",
        "price": "$27.99",
        "rating": "4.1★",
        "photo": "https://m.media-amazon.com/images/I/61pdOEI-mKL._AC_SL1500_.jpg",
        "url": "https://www.amazon.com/dp/B0C4FTJ1CN?tag=smartdeal0358-21"
    },
    {
        "asin": "B0CXSRT211",
        "title": "IOWER Boho Macrame Woven Wall Hanging Tapestry",
        "price": "$31.50",
        "rating": "4.4★",
        "photo": "https://m.media-amazon.com/images/I/71wK8n+3mKL._AC_SL1500_.jpg",
        "url": "https://www.amazon.com/dp/B0CXSRT211?tag=smartdeal0358-21"
    },
    {
        "asin": "B0FRS84KT9",
        "title": "Acrylic Illuminated Glowing LED Note Memo Board",
        "price": "$29.99",
        "rating": "4.5★",
        "photo": "https://m.media-amazon.com/images/I/61WvMvN-PCL._AC_SL1500_.jpg",
        "url": "https://www.amazon.com/dp/B0FRS84KT9?tag=smartdeal0358-21"
    },
    {
        "asin": "B08HJ2M49T",
        "title": "Crystal Suncatcher Prism Window Hanging Decor",
        "price": "$14.99",
        "rating": "4.8★",
        "photo": "https://m.media-amazon.com/images/I/71Y+z+q2mSL._AC_SL1500_.jpg",
        "url": "https://www.amazon.com/dp/B08HJ2M49T?tag=smartdeal0358-21"
    }
]

print("🔍 === INSPECTING CANDIDATE AMAZON MAIN PHOTOS FOR WHITE BACKGROUND CUTOUTS ===")
results = []
for prod in candidates:
    is_lifestyle = is_lifestyle_photo(prod["photo"])
    prod["is_white_background"] = not is_lifestyle
    results.append(prod)
    status = "❌ White Background Cutout" if not is_lifestyle else "✅ Lifestyle Room Photo"
    print(f"[{prod['asin']}] {prod['title'][:45]}... -> {status}")

with open("white_bg_analysis.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
