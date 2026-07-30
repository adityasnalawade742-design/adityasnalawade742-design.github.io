from modules.amazon_finder import _fetch_from_serpapi

queries = [
    "volcanic flame diffuser humidifier",
    "acrylic illuminated glowing note board",
    "raining cloud raindrop humidifier",
    "candle warmer lamp with timer",
    "retro typewriter wireless keyboard"
]

print("=== SEARCHING VIRAL UNIQUE PINTEREST TRENDS ===")
for q in queries:
    res = _fetch_from_serpapi(q, num_results=2)
    if res:
        item = res[0]
        print(f"\n[UNIQUE TREND]: '{q.title()}'")
        print(f"Title: {item['title'][:60]}")
        print(f"ASIN: {item['id']} | Price: {item['price']} | Rating: {item['rating']}")
        print(f"URL: https://www.amazon.com/dp/{item['id']}?tag=smartdeal0358-21")
