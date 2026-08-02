"""Hit the live server /api/discover and print exactly what the browser receives."""
import requests, json

try:
    r = requests.get(
        "http://localhost:5000/api/discover",
        params={"query": "aesthetic mushroom lamp", "count": 3},
        timeout=30
    )
    print(f"HTTP Status: {r.status_code}")
    data = r.json()
    print(f"Status field: {data.get('status')}")
    items = data.get('items', [])
    print(f"Items count: {len(items)}\n")
    for it in items:
        print(f"  asin     : {it.get('asin')}")
        print(f"  title    : {it.get('title','')[:50]}")
        print(f"  thumbnail: {it.get('thumbnail','MISSING')[:80]}")
        print()
    if not items:
        print("RAW RESPONSE:", json.dumps(data, indent=2)[:800])
except Exception as e:
    print(f"ERROR hitting server: {e}")
