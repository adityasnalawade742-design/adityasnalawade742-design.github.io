import os
import sys
import io
import time
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

PINTEREST_ACCESS_TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN", "")

sys.path.append(str(BASE_DIR))
from modules.seo_copywriter import generate_pin_seo_data
from modules.pinterest_publisher import get_board_for_category, CATEGORY_BOARD_MAP

# Sandbox endpoint for Trial Access Tokens, Production for Standard Tokens
API_URL = "https://api-sandbox.pinterest.com/v5/pins"

BOARD_NAMES = {
    "1092545259543956197": "Boho Vases & Desk Decor",
    "1092545259543956233": "Aesthetic Lighting & Lamps",
    "1092545259543956238": "Vanity Mirrors & Wall Decor",
    "1092545259543956242": "Cozy Room & Home Decor"
}

reg_path = BASE_DIR / "product_price_registry.json"
registry = json.loads(reg_path.read_text(encoding="utf-8"))

headers = {
    "Authorization": f"Bearer {PINTEREST_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

print("=" * 70)
print(f"🚀 CATEGORY-ROUTED PUBLISHER: {len(registry)} HOMEPAGE PRODUCTS TO PINTEREST")
for cat, b_id in CATEGORY_BOARD_MAP.items():
    b_name = BOARD_NAMES.get(b_id, "Pinterest Board")
    print(f"  • Category [{cat:8s}] -> Board ID: {b_id} ({b_name})")
print("=" * 70)

results = []
for idx, (asin, data) in enumerate(registry.items(), 1):
    title = data.get("title", f"Cozy Room Decor Find {asin}")
    category = data.get("category", "decor")
    target_board_id = get_board_for_category(category)
    board_name = BOARD_NAMES.get(target_board_id, "Category Board")
    
    seo = generate_pin_seo_data(title)
    
    bridge_url = f"https://adityasnalawade742-design.github.io/bridge_{asin}.html"
    image_url = f"https://adityasnalawade742-design.github.io/focus_product_{asin}_hook.jpg"
    
    payload = {
        "title": seo["pin_title"][:100],
        "description": seo["description"][:800],
        "link": bridge_url,
        "board_id": target_board_id,
        "media_source": {
            "source_type": "image_url",
            "url": image_url
        }
    }
    
    print(f"\n[{idx}/{len(registry)}] ASIN: {asin} (Category: {category})")
    print(f"  📌 Target Board: '{board_name}' (ID: {target_board_id})")
    print(f"  ✍️ Title: {payload['title']}")
    print(f"  🔗 Link:  {bridge_url}")
    
    try:
        res = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        if res.status_code in [200, 201]:
            resp_data = res.json()
            pin_id = resp_data.get("id")
            print(f"  ✅ SUCCESS! Published Pin ID: {pin_id}")
            results.append({"asin": asin, "status": "published", "pin_id": pin_id, "board": board_name})
        else:
            # Fallback to Production endpoint if Sandbox returns 404
            res_prod = requests.post("https://api.pinterest.com/v5/pins", headers=headers, json=payload, timeout=15)
            if res_prod.status_code in [200, 201]:
                resp_data = res_prod.json()
                pin_id = resp_data.get("id")
                print(f"  ✅ SUCCESS (Production API)! Published Pin ID: {pin_id}")
                results.append({"asin": asin, "status": "published", "pin_id": pin_id, "board": board_name})
            else:
                print(f"  ⚠️ Error ({res.status_code}): {res.text}")
                results.append({"asin": asin, "status": "error", "response": res.text, "board": board_name})
    except Exception as e:
        print(f"  ❌ Exception: {e}")
        results.append({"asin": asin, "status": "exception", "error": str(e), "board": board_name})
        
    time.sleep(1.5)

print("\n" + "=" * 70)
published_count = sum(1 for r in results if r["status"] == "published")
print(f"🎉 CATEGORY BATCH PUBLISH COMPLETE: {published_count}/{len(registry)} pins published live across all 4 category boards!")
print("=" * 70)
