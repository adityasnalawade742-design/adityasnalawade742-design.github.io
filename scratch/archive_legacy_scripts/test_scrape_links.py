from modules.amazon_scraper import scrape_amazon_product

test_asins = ['B0BZXNSW5K', 'B0D1FRDFFX', 'B0D8P8CSYP', 'B0DXKGL1T2']

for asin in test_asins:
    url = f"https://www.amazon.com/dp/{asin}"
    try:
        data = scrape_amazon_product(url)
        print(f"ASIN {asin}: Title='{data['title'][:40]}' | Price={data.get('price')}")
    except Exception as e:
        print(f"ASIN {asin}: Error {e}")
