import sys
import json
import urllib.request

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

url = "http://localhost:5000/api/extract?target=B0D8P8CSYP"
print("🔍 Extracting photo suite for Sunset Projection Lamp (B0D8P8CSYP) via Web Console...\n")

req = urllib.request.urlopen(url)
res = json.loads(req.read().decode("utf-8"))

print(f"📦 Title: {res.get('title')}")
print(f"💰 Price: {res.get('price')}")
print(f"🏆 Winner Photo: {res.get('winner_photo')}")
print(f"📸 Total Photos Extracted: {len(res.get('photos', []))}\n")

for i, photo in enumerate(res.get('photos', []), 1):
    print(f"  [{i}] {photo['url']}")
    print(f"      Clean: {photo['is_clean']} | Status: {photo['status']}")
