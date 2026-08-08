import sys
import io
import json
from pathlib import Path
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent
soup = BeautifulSoup(open(repo_dir / "index.html", encoding="utf-8").read(), "html.parser")
cards = soup.find_all(class_="card-wrapper")
asins = [c.get("id").replace("card-", "") for c in cards]

registry = json.load(open(repo_dir / "product_price_registry.json", encoding="utf-8"))

print("==================================================")
print(f"📦 ALL {len(asins)} HOMEPAGE PRODUCTS - ASINs & LINKS")
print("==================================================")

for idx, asin in enumerate(asins, 1):
    meta = registry.get(asin, {})
    title = meta.get("title", f"Product {asin}")
    price = meta.get("current_price", "$19.99")
    amazon_link = f"https://www.amazon.com/dp/{asin}"
    bridge_link = f"https://adityasnalawade742-design.github.io/bridge_{asin}.html"

    print(f"\n{idx}. ASIN: {asin}")
    print(f"   Title:       {title}")
    print(f"   Price:       {price}")
    print(f"   Amazon Link: {amazon_link}")
    print(f"   Bridge Link: {bridge_link}")

print("\n==================================================")
