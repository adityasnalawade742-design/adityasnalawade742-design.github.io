import os
import sys
import json
import requests
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv(".env")
token = os.getenv("PINTEREST_ACCESS_TOKEN", "")

if not token:
    print("No PINTEREST_ACCESS_TOKEN found in .env")
    sys.exit(0)

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

print("==================================================")
print("📌 FETCHING USER'S PINTEREST BOARDS VIA API V5")
print("==================================================")

try:
    res = requests.get("https://api.pinterest.com/v5/boards", headers=headers, timeout=15)
    print(f"API Status Code: {res.status_code}")
    if res.status_code == 200:
        data = res.json()
        items = data.get("items", [])
        print(f"\nFound {len(items)} Board(s) on your Pinterest Account:\n")
        board_mapping = {}
        for b in items:
            b_id = b.get("id")
            b_name = b.get("name")
            board_mapping[b_name] = b_id
            print(f"  • Board Name: '{b_name}'")
            print(f"    Board ID:   {b_id}\n")
        
        # Save mapping for reference
        with open("pinterest_board_mapping.json", "w", encoding="utf-8") as f:
            json.dump(board_mapping, f, indent=2)
        print("Saved mapping to pinterest_board_mapping.json")
    else:
        print(f"API Error Response: {res.text}")
except Exception as e:
    print(f"Error connecting to Pinterest API: {e}")
