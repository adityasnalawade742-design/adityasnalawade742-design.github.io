import os
import json
import dotenv
from pathlib import Path

dotenv.load_dotenv()

BASE_DOMAIN = "https://adityasnalawade742-design.github.io"

BOARD_MAPPING = {
    "vases": "1092545259543956197",
    "lighting": "1092545259543956233",
    "mirror": "1092545259543956238",
    "decor": "1092545259543956242"
}

def export_sandbox_payload():
    registry_path = Path("product_price_registry.json")
    if not registry_path.exists():
        print("[-] Error: product_price_registry.json not found!")
        return

    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)

    sandbox_pins = []

    for asin, data in registry.items():
        title = data.get("title", f"Cozy Room Decor Find - {asin}")
        category = (data.get("category") or "decor").lower()
        board_id = BOARD_MAPPING.get(category, BOARD_MAPPING["decor"])
        
        us_price = data.get("price") or "$0.00"
        features = data.get("features", [])
        feature_text = " • ".join(features[:3]) if features else "Aesthetic Home Decor Find"
        
        description = f"Cozy Room Finds: {title}\n\nPrice: {us_price}\n{feature_text}\n\nAs an Amazon Associate, Cozy Room Finds earns from qualifying purchases."

        destination_url = f"{BASE_DOMAIN}/bridge_{asin}.html"
        image_url = f"{BASE_DOMAIN}/focus_product_{asin}_hook.jpg"

        pin_item = {
            "asin": asin,
            "category": category,
            "board_id": board_id,
            "endpoint": "https://api-sandbox.pinterest.com/v5/pins",
            "payload": {
                "board_id": board_id,
                "title": title[:100],
                "description": description[:800],
                "link": destination_url,
                "media_source": {
                    "source_type": "image_url",
                    "url": image_url
                }
            }
        }
        sandbox_pins.append(pin_item)

    with open("sandbox_pins_payload.json", "w", encoding="utf-8") as f:
        json.dump(sandbox_pins, f, indent=2)

    print(f"[+] Successfully exported {len(sandbox_pins)} Sandbox Pin payloads to sandbox_pins_payload.json")

if __name__ == "__main__":
    export_sandbox_payload()
