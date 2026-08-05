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
VASES_BOARD_ID = "1092545259543956197"  # Boho Vases & Desk Decor Board

sys.path.append(str(BASE_DIR))
from modules.seo_copywriter import generate_pin_seo_data

# Use Sandbox API for Trial Access Token, fallback to Production API
API_URL = "https://api-sandbox.pinterest.com/v5/pins"

reg_path = BASE_DIR / "product_price_registry.json"
registry = json.loads(reg_path.read_text(encoding="utf-8"))

# Filter strictly for vase products
vase_asins = ["B0C2YLN3H4", "B0C7WFZZ7D", "B0BXP7YWHJ", "B0D6YRJLCP"]
vase_items = {k: v for k, v in registry.items() if k in vase_asins or "vase" in v.get("title", "").lower()}

headers = {
    "Authorization": f"Bearer {PINTEREST_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

print("=" * 70)
print(f"🪴 PUBLISHING {len(vase_items)} VASE PRODUCTS TO 'Boho Vases & Desk Decor'")
print(f"📌 Target Board ID: {VASES_BOARD_ID}")
print(f"🌐 API Endpoint: {API_URL}")
print("=" * 70)

results = []
for idx, (asin, data) in enumerate(vase_items.items(), 1):
    title = data.get("title", f"Boho Ceramic Vase {asin}")
    seo = generate_pin_seo_data(title)
    
    bridge_url = f"https://adityasnalawade742-design.github.io/bridge_{asin}.html"
    image_url = f"https://adityasnalawade742-design.github.io/focus_product_{asin}_hook.jpg"
    
    payload = {
        "title": seo["pin_title"][:100],
        "description": seo["description"][:800],
        "link": bridge_url,
        "board_id": VASES_BOARD_ID,
        "media_source": {
            "source_type": "image_url",
            "url": image_url
        }
    }
    
    print(f"\n[{idx}/{len(vase_items)}] ASIN: {asin}")
    print(f"  📌 Title: {payload['title']}")
    print(f"  🔗 Link:  {bridge_url}")
    print(f"  🖼️ Image: {image_url}")
    
    try:
        res = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        if res.status_code in [200, 201]:
            resp_data = res.json()
            pin_id = resp_data.get("id")
            print(f"  ✅ SUCCESS! Published Pin ID: {pin_id}")
            results.append({"asin": asin, "status": "published", "pin_id": pin_id})
        else:
            # Fallback to Production endpoint if Sandbox returns 404
            res_prod = requests.post("https://api.pinterest.com/v5/pins", headers=headers, json=payload, timeout=15)
            if res_prod.status_code in [200, 201]:
                resp_data = res_prod.json()
                pin_id = resp_data.get("id")
                print(f"  ✅ SUCCESS (Production API)! Published Pin ID: {pin_id}")
                results.append({"asin": asin, "status": "published", "pin_id": pin_id})
            else:
                print(f"  ⚠️ Error ({res.status_code}): {res.text}")
                results.append({"asin": asin, "status": "error", "response": res.text})
    except Exception as e:
        print(f"  ❌ Exception: {e}")
        results.append({"asin": asin, "status": "exception", "error": str(e)})
        
    time.sleep(1.5)

print("\n" + "=" * 70)
published_count = sum(1 for r in results if r["status"] == "published")
print(f"🎉 VASE BOARD PUBLISH COMPLETE: {published_count}/{len(vase_items)} pins published live to Boho Vases & Desk Decor!")
print("=" * 70)
