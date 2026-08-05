import os
import json
import requests
from pathlib import Path
from config import PINTEREST_ACCESS_TOKEN, PINTEREST_BOARD_ID

PINTEREST_API_ENDPOINT = "https://api.pinterest.com/v5/pins"

CATEGORY_BOARD_MAP = {
    "vases": "1092545259543956197",       # Boho Vases & Desk Decor
    "lighting": "1092545259543956233",    # Aesthetic Lighting & Lamps
    "mirror": "1092545259543956238",      # Vanity Mirrors & Wall Decor
    "decor": "1092545259543956242"        # Cozy Room & Home Decor
}

def get_board_for_category(category: str = "decor") -> str:
    cat = (category or "decor").lower()
    for key, board_id in CATEGORY_BOARD_MAP.items():
        if key in cat:
            return board_id
    return PINTEREST_BOARD_ID or "1092545259543956197"

def publish_pin_to_pinterest(
    image_path: str,
    title: str,
    description: str,
    destination_url: str,
    board_id: str = None,
    access_token: str = None,
    image_url: str = None,
    category: str = "decor"
) -> dict:
    """
    Publishes a pin directly via Pinterest API v5 if credentials are present in config or parameters.
    Otherwise formats a Pin Payload ready for scheduling via Make/n8n/Buffer.
    Automatically routes to category-specific Board ID if board_id is omitted.
    """
    token = access_token or PINTEREST_ACCESS_TOKEN
    target_board_id = board_id or get_board_for_category(category)

    # M8 FIX: if no image URL, refuse to publish — Pinterest API rejects HTML page URLs
    if not image_url:
        print(f"[Pinterest Publisher] ⚠️ No image_url provided. Skipping live publish — Pinterest API requires a direct .jpg/.png URL.")
        return {"status": "SKIPPED_NO_IMAGE", "reason": "image_url is required for Pinterest API", "title": title}

    # Media URL for Pinterest pin creation
    media_url = image_url

    safe_title = (title or "")[:100]
    safe_desc = (description or "")[:800]

    if title and len(title) > 100:
        print(f"[Pinterest Publisher] ℹ️ Title truncated from {len(title)} to 100 characters for Pinterest API compliance.")
    if description and len(description) > 800:
        print(f"[Pinterest Publisher] ℹ️ Description truncated from {len(description)} to 800 characters for Pinterest API compliance.")

    # H5 FIX: only include board_id in payload when it is a real ID (not a placeholder or empty)
    pin_payload = {
        "title": safe_title,  # Pinterest max title length
        "description": safe_desc,
        "link": destination_url,
        "media_source": {
            "source_type": "image_url",
            "url": media_url
        }
    }
    if target_board_id and target_board_id.isdigit():
        pin_payload["board_id"] = target_board_id
    elif target_board_id:
        print(f"[Pinterest Publisher] ⚠️ Warning: Board ID '{target_board_id}' appears to be a board name, not a numeric Pinterest Board ID. Pinterest API requires a numeric Board ID.")

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
                try:
                    data = res.json()
                    print(f"[Pinterest Publisher] ✅ Successfully posted Pin ID: {data.get('id', 'N/A')}")
                    return {"status": "PUBLISHED_LIVE", "pin_id": data.get("id"), "response": data}
                except Exception:
                    return {"status": "PUBLISHED_LIVE", "pin_id": "UNKNOWN", "response": res.text}
            else:
                print(f"[Pinterest Publisher] ⚠️ API returned error ({res.status_code}): {res.text}")
                return {"status": "API_ERROR", "status_code": res.status_code, "error": res.text, "payload": pin_payload}
        except Exception as e:
            print(f"[Pinterest Publisher] ❌ Exception connecting to Pinterest API: {e}")
            return {"status": "API_ERROR", "error": str(e), "payload": pin_payload}

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

