import sys, io, requests
from config import PINTEREST_ACCESS_TOKEN

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

print("✨ CREATING LIVE PINTEREST BOARD VIA API V5...")

headers = {
    "Authorization": f"Bearer {PINTEREST_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "name": "Cozy Room & Desk Decor",
    "description": "Curated aesthetic room finds, cozy bedside lighting, vanity mirrors, and luxury desk setup decor.",
    "privacy": "PUBLIC"
}

res = requests.post("https://api.pinterest.com/v5/boards", headers=headers, json=payload, timeout=10)
print(f"Status Code: {res.status_code}")
if res.status_code in [200, 201]:
    data = res.json()
    print("✅ SUCCESS! Created Live Pinterest Board:")
    print(f"   Board Name: '{data.get('name')}'")
    print(f"   Board ID:   {data.get('id')}")
else:
    print(f"Response: {res.text}")
