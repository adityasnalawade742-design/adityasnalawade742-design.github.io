import sys, io, requests
from config import PINTEREST_ACCESS_TOKEN, PINTEREST_BOARD_ID

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

print("🚀 PUBLISHING LIVE TEST PIN TO PINTEREST VIA API V5...")
print(f"Target Board ID: {PINTEREST_BOARD_ID}")

headers = {
    "Authorization": f"Bearer {PINTEREST_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "title": "Cozy White Ceramic Donut Vase ✨",
    "description": "Discover viral aesthetic room upgrades & boho table decor finds for the ultimate cozy bedroom setup!",
    "link": "https://adityasnalawade742-design.github.io/bridge_B0C2YLN3H4.html",
    "board_id": PINTEREST_BOARD_ID,
    "media_source": {
        "source_type": "image_url",
        "url": "https://adityasnalawade742-design.github.io/focus_product_B0C2YLN3H4_hook.jpg"
    }
}

res = requests.post("https://api.pinterest.com/v5/pins", headers=headers, json=payload, timeout=15)
print(f"API Response Code: {res.status_code}")
if res.status_code in [200, 201]:
    data = res.json()
    print("\n🎉 SUCCESS! LIVE PIN PUBLISHED ON PINTEREST:")
    print(f"   Pin ID:      {data.get('id')}")
    print(f"   Pin Link:    https://www.pinterest.com/pin/{data.get('id')}/")
    print(f"   Board ID:    {data.get('board_id')}")
else:
    print(f"❌ Error: {res.text}")
