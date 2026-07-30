from modules.amazon_extractor import get_product_details_and_photos

new_asins = ['B099KFCK9F', 'B09ZP4MCRV', 'B0B5D98Z5P', 'B0B7BPG1KP', 'B0C6T8T1LN']

print("Verifying 5 NEW unprocessed Amazon products:")
for asin in new_asins:
    try:
        data = get_product_details_and_photos(asin)
        if data and data.get('title'):
            print(f"[NEW PRODUCT] ASIN: {asin} | Title: '{data['title'][:45]}' | Price: {data.get('price')} | URL: https://www.amazon.com/dp/{asin}?tag=adityasnalawa-20")
        else:
            print(f"[FAILED] ASIN: {asin}")
    except Exception as e:
        print(f"[ERROR] ASIN: {asin} -> {e}")
