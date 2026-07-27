import os
import sys
import io
import time
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
from modules.seo_copywriter import generate_pin_seo_data

BASE_DIR = Path(__file__).resolve().parent

PINTEREST_BOARD_ID = os.getenv("PINTEREST_BOARD_ID", "1092545259543920271")
PINTEREST_ACCESS_TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN", "")


API_URL = "https://api-sandbox.pinterest.com/v5/pins"

SELECTED_5_PRODUCTS = [
    {
        "asin": "B0GYDXHF4G",
        "title": "Flame Aroma Diffuser, Dark Crackle Design, Flame Effect Humidifier",
        "bridge": "https://adityasnalawade742-design.github.io/bridge_B0GYDXHF4G.html",
        "image": "https://adityasnalawade742-design.github.io/focus_product_B0GYDXHF4G_hook.jpg"
    },
    {
        "asin": "B0FXLYXM32",
        "title": "Pocetry 22\"x30\" White Wavy Wall Mirror for Vanity, Cream Solid Wood Irregular Mirror",
        "bridge": "https://adityasnalawade742-design.github.io/bridge_B0FXLYXM32.html",
        "image": "https://adityasnalawade742-design.github.io/focus_product_B0FXLYXM32_hook.jpg"
    },
    {
        "asin": "B0C2YLN3H4",
        "title": "White Ceramic Donut Vase Set of 2, Hollow Matte Pampas Flower Vases",
        "bridge": "https://adityasnalawade742-design.github.io/bridge_B0C2YLN3H4.html",
        "image": "https://adityasnalawade742-design.github.io/focus_product_B0C2YLN3H4_exact2vases_hook.jpg"
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
    }
]

UNPOSTED_REMAINING_5 = [
    {"asin": "B0GGHJ1J4L", "title": "Led Note Board with Colors Acrylic Set Glowing Desktop Sign Letter Memo"},
    {"asin": "B0BZXNSW5K", "title": "Fenmzee Bedside Table Touch Lamp Dimmable Ambient Nightstand Light"},
    {"asin": "B0DXKGL1T2", "title": "Lily of the Valley Flower Table Lamp Aesthetic Floral Nightstand Accent"},
    {"asin": "B0D1FRDFFX", "title": "Dawnwake Mushroom Touch Table Lamp Glass Dome Bedside Glow"},
    {"asin": "B0D8P8CSYP", "title": "Cute Bird Dimmable Touch Night Lamp Rechargeable Bedside Light"}
]

def publish_5():
    headers = {
        "Authorization": f"Bearer {PINTEREST_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    posted_list = []
    for idx, p in enumerate(SELECTED_5_PRODUCTS, 1):
        seo = generate_pin_seo_data(p["title"])
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
                posted_list.append({
                    "asin": p["asin"],
                    "status": "POSTED",
                    "pin_id": pin_id,
                    "pin_title": seo["pin_title"],
                    "description": seo["description"],
                    "link": p["bridge"],
                    "image": p["image"]
                })
            else:
                posted_list.append({
                    "asin": p["asin"],
                    "status": "ERROR",
                    "status_code": res.status_code,
                    "response": res.text
                })
        except Exception as e:
            posted_list.append({
                "asin": p["asin"],
                "status": "EXCEPTION",
                "error": str(e)
            })
        
        time.sleep(1)

    tracker = {
        "posted_products": posted_list,
        "unposted_products": [
            {
                "asin": p["asin"],
                "status": "UNPOSTED",
                "title": p["title"]
            } for p in UNPOSTED_REMAINING_5
        ]
    }

    with open(BASE_DIR / "pinterest_campaign_tracker.json", "w", encoding="utf-8") as f:
        json.dump(tracker, f, indent=2)

if __name__ == "__main__":
    publish_5()
