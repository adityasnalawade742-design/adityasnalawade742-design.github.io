import os
import sys
import json
import time
import requests
import dotenv
from pathlib import Path

# Load environment variables
dotenv.load_dotenv()

PINTEREST_ACCESS_TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN")
PINTEREST_SANDBOX_TOKEN = os.getenv("PINTEREST_SANDBOX_ACCESS_TOKEN") or PINTEREST_ACCESS_TOKEN
PINTEREST_SANDBOX_BOARD_ID = os.getenv("PINTEREST_SANDBOX_BOARD_ID") or "1092545259543959836"

PROD_ENDPOINT = "https://api.pinterest.com/v5/pins"
SANDBOX_ENDPOINT = "https://api-sandbox.pinterest.com/v5/pins"

BASE_DOMAIN = "https://adityasnalawade742-design.github.io"

# Production Category to Board ID mapping
PROD_BOARD_MAPPING = {
    "vases": "1092545259543956197",     # Boho Vases & Desk Decor
    "lighting": "1092545259543956233",  # Aesthetic Lighting & Lamps
    "mirror": "1092545259543956238",    # Vanity Mirrors & Wall Decor
    "decor": "1092545259543956242"      # Cozy Room & Home Decor
}

def publish_all_homepage_products(mode: str = "sandbox"):
    registry_path = Path("product_price_registry.json")
    if not registry_path.exists():
        print("[-] Error: product_price_registry.json not found!")
        return

    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)

    is_sandbox = (mode.lower() == "sandbox")
    endpoint = SANDBOX_ENDPOINT if is_sandbox else PROD_ENDPOINT
    token = PINTEREST_SANDBOX_TOKEN if is_sandbox else PINTEREST_ACCESS_TOKEN

    print(f"[*] STARTING PINTEREST PUBLISHER IN [{mode.upper()}] MODE...")
    print(f"    Target Endpoint: {endpoint}")
    print(f"    Total Products:  {len(registry)}\n")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    published_count = 0
    failed_count = 0
    results = []

    for asin, data in registry.items():
        title = data.get("title", f"Cozy Room Decor Find - {asin}")
        category = (data.get("category") or "decor").lower()
        
        # Sandbox mode uses PINTEREST_SANDBOX_BOARD_ID ("1092545259543959836")
        board_id = PINTEREST_SANDBOX_BOARD_ID if is_sandbox else PROD_BOARD_MAPPING.get(category, PROD_BOARD_MAPPING["decor"])
        
        us_price = data.get("price") or "$0.00"
        features = data.get("features", [])
        feature_text = " • ".join(features[:3]) if features else "Aesthetic Home Decor Find"
        
        description = f"Cozy Room Finds: {title}\n\nPrice: {us_price}\n{feature_text}\n\nAs an Amazon Associate, Cozy Room Finds earns from qualifying purchases."

        destination_url = f"{BASE_DOMAIN}/bridge_{asin}.html"
        image_url = f"{BASE_DOMAIN}/focus_product_{asin}_hook.jpg"

        payload = {
            "board_id": board_id,
            "title": title[:100],
            "description": description[:800],
            "link": destination_url,
            "media_source": {
                "source_type": "image_url",
                "url": image_url
            }
        }

        print(f"[>] [{mode.upper()}] Publishing ASIN [{asin}] ({category.upper()}) to Board [{board_id}]...")
        print(f"    Title:  {title[:60]}...")
        print(f"    Image:  {image_url}")
        print(f"    Bridge: {destination_url}")

        try:
            res = requests.post(endpoint, headers=headers, json=payload, timeout=15)
            if res.status_code in (200, 201):
                res_data = res.json()
                pin_id = res_data.get("id", "UNKNOWN")
                print(f"    [+] SUCCESS! Pin ID: {pin_id}\n")
                published_count += 1
                results.append({"asin": asin, "status": "SUCCESS", "pin_id": pin_id, "board_id": board_id, "title": title, "category": category, "mode": mode})
            else:
                print(f"    [-] FAILED! ({res.status_code}): {res.text}\n")
                failed_count += 1
                results.append({"asin": asin, "status": "FAILED", "code": res.status_code, "error": res.text, "mode": mode})
        except Exception as e:
            print(f"    [-] EXCEPTION: {e}\n")
            failed_count += 1
            results.append({"asin": asin, "status": "ERROR", "error": str(e), "mode": mode})

        time.sleep(1.5)

    print("==================================================")
    print(f"PINTEREST PIN PUBLISHING REPORT ({mode.upper()} MODE):")
    print("==================================================")
    print(f"Published: {published_count} / {len(registry)}")
    print(f"Failed:    {failed_count} / {len(registry)}")

    with open("pinterest_campaign_tracker.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("Saved campaign results to pinterest_campaign_tracker.json")

if __name__ == "__main__":
    mode_arg = sys.argv[1] if len(sys.argv) > 1 else "sandbox"
    publish_all_homepage_products(mode=mode_arg)
