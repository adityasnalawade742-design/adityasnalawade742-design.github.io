import re
import json
import sys
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

urls = [
    ("lighting", "https://in.pinterest.com/Nesteraliving/aesthetic-lighting-lamps/"),
    ("mirror", "https://in.pinterest.com/Nesteraliving/vanity-mirrors-wall-decor/"),
    ("decor", "https://in.pinterest.com/Nesteraliving/cozy-room-home-decor/")
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

board_map = {
    "vases": "1092545259543956197"  # Boho Vases & Desk Decor
}

print("==================================================")
print("EXTRACTING NUMERIC BOARD IDS FOR ALL CATEGORIES")
print("==================================================")

for cat_name, url in urls:
    try:
        res = requests.get(url, headers=headers, timeout=10)
        print(f"\nProcessing {cat_name} board ({url})...")
        
        matches = set()
        for pattern in [
            r'"board_id":\s*"(\d+)"',
            r'"boardId":\s*"(\d+)"',
            r'"id":\s*"(\d{15,20})"',
            r'board_id=(\d+)',
            r'/boards/(\d+)/'
        ]:
            found = re.findall(pattern, res.text)
            for f in found:
                if f != "1092545328261391769":  # Exclude user account ID
                    matches.add(f)
                    
        print(f"   Matches for {cat_name}: {list(matches)}")
        if matches:
            board_map[cat_name] = list(matches)[0]
    except Exception as e:
        print(f"   Error fetching {url}: {e}")

print("\n==================================================")
print("FINAL COMPLETE CATEGORY-TO-BOARD MAPPING:")
print(json.dumps(board_map, indent=2))
print("==================================================")

with open("pinterest_board_mapping.json", "w", encoding="utf-8") as f:
    json.dump(board_map, f, indent=2)
