import os
import sys
import io
import time
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
from modules.seo_copywriter import generate_pin_seo_data

# UTF-8 stdout
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

PINTEREST_BOARD_ID = os.getenv("PINTEREST_BOARD_ID", "1092545259543920271")
# Check if using Sandbox or Production token
PINTEREST_ACCESS_TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN", "")

API_URL = "https://api-sandbox.pinterest.com/v5/pins" if PINTEREST_ACCESS_TOKEN.startswith("pina_") else "https://api.pinterest.com/v5/pins"

HOMEPAGE_PRODUCTS = [
    {
        "asin": "B0GGHJ1J4L",
        "title": "Led Note Board with Colors Acrylic Set Glowing Desktop Sign Letter Memo Painting Manual",
        "bridge": "https://adityasnalawade742-design.github.io/bridge_B0GGHJ1J4L.html",
        "image": "https://adityasnalawade742-design.github.io/focus_product_B0GGHJ1J4L_hook.jpg"
    },
    {
        "asin": "B0C2YLN3H4",
        "title": "White Ceramic Donut Vase Set of 2, Hollow Matte Pampas Flower Vases",
        "bridge": "https://adityasnalawade742-design.github.io/bridge_B0C2YLN3H4.html",
        "image": "https://adityasnalawade742-design.github.io/focus_product_B0C2YLN3H4_exact2vases_hook.jpg"
    },
    {
        "asin": "B0FXLYXM32",
        "title": "Pocetry 22\"x30\" White Wavy Wall Mirror for Vanity, Cream Solid Wood Irregular Mirror",
        "bridge": "https://adityasnalawade742-design.github.io/bridge_B0FXLYXM32.html",
        "image": "https://adityasnalawade742-design.github.io/focus_product_B0FXLYXM32_hook.jpg"
    },
    {
        "asin": "B0GYDXHF4G",
        "title": "Flame Aroma Diffuser, Dark Crackle Design, Flame Effect Humidifier",
        "bridge": "https://adityasnalawade742-design.github.io/bridge_B0GYDXHF4G.html",
        "image": "https://adityasnalawade742-design.github.io/focus_product_B0GYDXHF4G_hook.jpg"
    },
    {
        "asin": "B07HP22QTZ",
        "title": "Suncatcher Crystals Ball Prism Window Rainbow Maker with Chain",
        "bridge": "https://adityasnalawade742-design.github.io/bridge_B07HP22QTZ.html",
        "image": "https://adityasnalawade742-design.github.io/focus_product_B07HP22QTZ_hook.jpg"
    },
    {
        "asin": "B0BDRSG2BT",
        "title": "Tsrarey Sunset Lamp Projection, Not Only 21 Colors Sunset Lights",
        "bridge": "https://adityasnalawade742-design.github.io/bridge_B0BDRSG2BT.html",
        "image": "https://adityasnalawade742-design.github.io/focus_product_B0BDRSG2BT_hook.jpg"
    },
    {
        "asin": "B0BZXNSW5K",
        "title": "Fenmzee Bedside Table Touch Lamp Dimmable Ambient Nightstand Light",
        "bridge": "https://adityasnalawade742-design.github.io/bridge_B0BZXNSW5K.html",
        "image": "https://adityasnalawade742-design.github.io/focus_product_B0BZXNSW5K_hook.jpg"
    },
    {
        "asin": "B0DXKGL1T2",
        "title": "Lily of the Valley Flower Table Lamp Aesthetic Floral Nightstand Accent",
        "bridge": "https://adityasnalawade742-design.github.io/bridge_B0DXKGL1T2.html",
        "image": "https://adityasnalawade742-design.github.io/focus_product_B0DXKGL1T2_hook.jpg"
    },
    {
        "asin": "B0D1FRDFFX",
        "title": "Dawnwake Mushroom Touch Table Lamp Glass Dome Bedside Glow",
        "bridge": "https://adityasnalawade742-design.github.io/bridge_B0D1FRDFFX.html",
        "image": "https://adityasnalawade742-design.github.io/focus_product_B0D1FRDFFX_hook.jpg"
    },
    {
        "asin": "B0D8P8CSYP",
        "title": "Cute Bird Dimmable Touch Night Lamp Rechargeable Bedside Light",
        "bridge": "https://adityasnalawade742-design.github.io/bridge_B0D8P8CSYP.html",
        "image": "https://adityasnalawade742-design.github.io/focus_product_B0D8P8CSYP_hook.jpg"
    }
]

def publish_all():
    print("=" * 70)
    print("🚀 BATCH POSTING ALL 10 HOMEPAGE PRODUCTS WITH HIGH-REACH VIRAL SEO COPY")
    print(f"📌 Board ID: {PINTEREST_BOARD_ID}")
    print(f"🌐 API Endpoint: {API_URL}")
    print("=" * 70)

    headers = {
        "Authorization": f"Bearer {PINTEREST_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    results = []
    for idx, p in enumerate(HOMEPAGE_PRODUCTS, 1):
        seo = generate_pin_seo_data(p["title"])
        print(f"\n[{idx}/10] ASIN: {p['asin']}")
        print(f"  📌 Title: {seo['pin_title']}")
        print(f"  ✍️ Desc:  {seo['description'][:80]}...")
        
        payload = {
            "title": seo["pin_title"][:100],
            "description": seo["description"][:800],
            "link": p["bridge"],
            "board_id": PINTEREST_BOARD_ID,
            "media_source": {
                "source_type": "image_url",
                "url": p["image"]
            }
        }

        try:
            res = requests.post(API_URL, headers=headers, json=payload, timeout=15)
            if res.status_code in [200, 201]:
                data = res.json()
                pin_id = data.get("id")
                print(f"  ✅ SUCCESS! Published Pin ID: {pin_id}")
                results.append({"asin": p["asin"], "status": "published", "pin_id": pin_id})
            else:
                print(f"  ⚠️ Error ({res.status_code}): {res.text}")
                results.append({"asin": p["asin"], "status": "error", "response": res.text})
        except Exception as e:
            print(f"  ❌ Exception: {e}")
            results.append({"asin": p["asin"], "status": "exception", "error": str(e)})
        
        time.sleep(1)

    print("\n" + "=" * 70)
    print(f"🎉 COMPLETED: Processed all {len(results)} homepage products!")
    print("=" * 70)

if __name__ == "__main__":
    publish_all()
