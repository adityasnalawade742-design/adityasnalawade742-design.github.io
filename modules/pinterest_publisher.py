import os
import json
import requests
from pathlib import Path
from config import PINTEREST_ACCESS_TOKEN, PINTEREST_BOARD_ID

PINTEREST_API_ENDPOINT = "https://api.pinterest.com/v5/pins"

CATEGORY_BOARD_MAP = {
    "lighting": "Aesthetic Lighting & Lamps",
    "vases": "Boho Vases & Desk Decor",
    "mirror": "Vanity Mirrors & Wall Decor",
    "decor": "Cozy Room & Home Decor"
}

def get_board_for_category(category: str = "decor") -> str:
    cat = (category or "decor").lower()
    for key, board in CATEGORY_BOARD_MAP.items():
        if key in cat:
            return board
    return "Cozy Room & Home Decor"

def publish_pin_to_pinterest(
    image_path: str,
    title: str,
    description: str,
    destination_url: str,
    board_id: str = None,
    access_token: str = None,
    image_url: str = None
) -> dict:
    """
    Publishes a pin directly via Pinterest API v5 if credentials are present in config or parameters.
    Otherwise formats a Pin Payload ready for scheduling via Make/n8n/Buffer.
    """
    token = access_token or PINTEREST_ACCESS_TOKEN
    target_board_id = board_id or PINTEREST_BOARD_ID

    # M8 FIX: if no image URL, refuse to publish — Pinterest API rejects HTML page URLs
    if not image_url:
        print(f"[Pinterest Publisher] ⚠️ No image_url provided. Skipping live publish — Pinterest API requires a direct .jpg/.png URL.")
        return {"status": "SKIPPED_NO_IMAGE", "reason": "image_url is required for Pinterest API", "title": title}

    # Media URL for Pinterest pin creation
    media_url = image_url

    # H5 FIX: only include board_id in payload when it is a real ID (not a placeholder or empty)
    pin_payload = {
        "title": title[:100],  # Pinterest max title length
        "description": description[:800],
        "link": destination_url,
        "media_source": {
            "source_type": "image_url",
            "url": media_url
        }
    }
    if target_board_id:
        pin_payload["board_id"] = target_board_id

    if token and target_board_id and target_board_id != "COZY_ROOM_DECOR_BOARD_ID":
        print(f"[Pinterest Publisher] 🚀 Attempting live API pin publish to board '{target_board_id}'...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        try:
            res = requests.post(PINTEREST_API_ENDPOINT, headers=headers, json=pin_payload, timeout=15)
            print(f"[Pinterest Publisher] API Status Code: {res.status_code}")
            if res.status_code in (200, 201):
                data = res.json()
                print(f"[Pinterest Publisher] ✅ Successfully posted Pin ID: {data.get('id', 'N/A')}")
                return {"status": "PUBLISHED_LIVE", "pin_id": data.get("id"), "response": data}
            else:
                print(f"[Pinterest Publisher] ⚠️ API returned error ({res.status_code}): {res.text}")
                return {"status": "API_ERROR", "status_code": res.status_code, "error": res.text, "payload": pin_payload}
        except Exception as e:
            print(f"[Pinterest Publisher] ❌ Exception connecting to Pinterest API: {e}")

    # Ready payload output for manual / buffer / n8n / make publishing
    report = {
        "status": "READY_FOR_PUBLISH",
        "title": title,
        "description": description,
        "bridge_destination_link": destination_url,
        "image_file": str(image_path),
        "payload": pin_payload
    }
    print(f"[Pinterest Publisher] 📝 Prepared Pin Payload (no live API token provided yet): {title[:40]}...")
    return report

