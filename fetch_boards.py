import sys, io, os, requests
from config import PINTEREST_ACCESS_TOKEN

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

print("🔍 CONNECTING TO PINTEREST API V5...")
print(f"Token: {PINTEREST_ACCESS_TOKEN[:15]}...\n")

headers = {
    "Authorization": f"Bearer {PINTEREST_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# 1. Fetch Pinner Profile
try:
    res_user = requests.get("https://api.pinterest.com/v5/user_account", headers=headers, timeout=10)
    print(f"User Account API Status: {res_user.status_code}")
    if res_user.status_code == 200:
        u_data = res_user.json()
        print(f"✅ Authenticated Pinterest User: @{u_data.get('username')} ({u_data.get('account_type')})")
    else:
        print(f"User API Response: {res_user.text}")
except Exception as e:
    print(f"Error fetching user profile: {e}")

print("-" * 50)

# 2. Fetch Live Boards
try:
    res_boards = requests.get("https://api.pinterest.com/v5/boards", headers=headers, timeout=10)
    print(f"Boards API Status: {res_boards.status_code}")
    if res_boards.status_code == 200:
        b_data = res_boards.json()
        items = b_data.get("items", [])
        print(f"\n📋 FOUND {len(items)} LIVE PINTEREST BOARDS:")
        for b in items:
            print(f"  • Board Name: '{b.get('name')}'")
            print(f"    Board ID:   {b.get('id')}\n")
    else:
        print(f"Boards API Response: {res_boards.text}")
except Exception as e:
    print(f"Error fetching boards: {e}")
