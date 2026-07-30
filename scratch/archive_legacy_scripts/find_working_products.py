from modules.amazon_extractor import get_product_details_and_photos

urls = [
    'https://www.amazon.com/dp/B0BZXNSW5K', # Fenmzee Touch Lamp (Verified working)
    'B0D1FRDFFX', # Mushroom Touch Lamp
    'B0D8P8CSYP', # Bird Touch Lamp
    'B0DXKGL1T2'  # Lily of Valley Flower Lamp
]

for u in urls:
    try:
        data = get_product_details_and_photos(u)
        if data:
            print(f"ASIN {data['asin']}: Title='{data['title'][:45]}' | Price={data.get('price')} | Photos={len(data['images'])}")
    except Exception as e:
        print(f"ASIN {u}: Error {e}")
