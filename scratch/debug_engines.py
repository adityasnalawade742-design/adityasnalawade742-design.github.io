"""
Deep debug: test what SerpAPI actually returns and why images are missing.
Tests both the google engine (current) and amazon engine (better).
"""
import sys, json, requests
sys.path.insert(0, '.')
from config import SERPAPI_KEYS

KEY = SERPAPI_KEYS[0]

print("=" * 60)
print("TEST 1: Google engine (current approach)")
print("=" * 60)
r = requests.get("https://serpapi.com/search.json", params={
    "engine": "google",
    "q": "site:amazon.com/dp candle warmer lamp timer buy",
    "api_key": KEY,
    "gl": "us", "hl": "en", "num": 5
}, timeout=15)
data = r.json()
results = data.get("organic_results", [])
print(f"Results count: {len(results)}")
for i, it in enumerate(results[:4]):
    thumb = it.get("thumbnail", "")
    img   = it.get("image", "")
    link  = it.get("link", "")[:60]
    title = it.get("title", "")[:40]
    print(f"\n  [{i+1}] {title}")
    print(f"       link      : {link}")
    print(f"       thumbnail : {thumb[:70] if thumb else 'EMPTY'}")
    print(f"       image     : {img[:70] if img else 'EMPTY'}")

print()
print("=" * 60)
print("TEST 2: Amazon engine (better approach)")
print("=" * 60)
r2 = requests.get("https://serpapi.com/search.json", params={
    "engine": "amazon",
    "k": "candle warmer lamp timer",
    "api_key": KEY,
    "amazon_domain": "amazon.com"
}, timeout=15)
data2 = r2.json()
results2 = data2.get("organic_results", [])
print(f"Results count: {len(results2)}")
for i, it in enumerate(results2[:4]):
    thumb = it.get("thumbnail", "")
    asin  = it.get("asin", "")
    price = it.get("price", "")
    rating = it.get("rating", "")
    title = it.get("title", "")[:45]
    print(f"\n  [{i+1}] ASIN: {asin} | Price: {price} | Rating: {rating}")
    print(f"       Title    : {title}")
    print(f"       thumbnail: {thumb[:70] if thumb else 'EMPTY'}")
