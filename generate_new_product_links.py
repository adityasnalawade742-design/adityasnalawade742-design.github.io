from modules.amazon_extractor import get_product_details_and_photos

new_items = [
    {"asin": "B099KFCK9F", "title": "Fire Flame Essential Oil Diffuser & Humidifier", "price": "$22.99"},
    {"asin": "B0BCW7CR43", "title": "Vintage Glass Mushroom Touch Desk Lamp", "price": "$29.99"},
    {"asin": "B0B5D98Z5P", "title": "Golden Hour Sunset Projection Lamp Light", "price": "$17.99"},
    {"asin": "B0B7BPG1KP", "title": "Acrylic Illuminated Glowing LED Note Board", "price": "$16.99"},
    {"asin": "B0BDLMBCHL", "title": "Dimmable Candle Warmer Lamp with Timer", "price": "$32.99"}
]

tag = "smartdeal0358-21"

print("=== NEW UNPROCESSED PRODUCTS WITH YOUR AFFILIATE STORE ID ===")
for item in new_items:
    a = item["asin"]
    url = f"https://www.amazon.com/dp/{a}?tag={tag}"
    search_url = f"https://www.amazon.com/s?k={a}&tag={tag}"
    print(f"Product: {item['title']} ({item['price']})")
    print(f"Direct Affiliate URL: {url}")
    print(f"Search URL: {search_url}\n")
