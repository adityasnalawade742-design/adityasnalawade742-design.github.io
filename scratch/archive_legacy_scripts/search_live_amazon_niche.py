from modules.amazon_finder import _fetch_from_serpapi

print("[Live Search] Searching Live Amazon Catalog via SerpAPI for: 'cozy ambient bedside lamp'...")
results = _fetch_from_serpapi("cozy ambient bedside lamp", num_results=5)

if results:
    print("\n=== LIVE ACTIVE AMAZON PRODUCTS FOUND ===")
    for item in results:
        print(f"Title: {item['title']}")
        print(f"ASIN: {item['id']} | Price: {item['price']} | Rating: {item['rating']}")
        print(f"Affiliate URL: {item['affiliate_url']}\n")
else:
        print("No live items returned.")
