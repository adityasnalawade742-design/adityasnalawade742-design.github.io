import sys
import json
from pathlib import Path
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")
index_file = repo / "index.html"
registry_file = repo / "product_price_registry.json"

print("=== 📌 ADDING data-direct-regions TO ALL HOMEPAGE CARD WRAPPERS ===")

direct_regions_map = {
    "B0DZD1X83N": "US,DE,SE,CA,JP",
    "B0BZXNSW5K": "US,IN,UK,DE,SE,CA,JP",
    "B0D1FRDFFX": "US,IN,UK,DE,SE,SG,CA,AU,JP",
    "B0C2YLN3H4": "US,IN,DE,SE,SG,CA,AU,JP",
    "B0GYDXHF4G": "US,DE,SE,CA,JP",
    "B0FXLYXM32": "US,IN,UK,DE,SE,SG,CA,AU,JP",
    "B07HP22QTZ": "US,IN,GB,UK,DE,SE,SG,CA,AU,JP",
    "B0D8P8CSYP": "US,IN,UK,DE,SE,SG,CA,AU,JP",
    "B0DXKGL1T2": "US,UK,DE,SE,CA,JP"
}

index_html = index_file.read_text(encoding="utf-8")
soup = BeautifulSoup(index_html, "html.parser")

for card in soup.find_all("div", class_="card-wrapper"):
    asin = card.get("data-asin") or card.get("id", "").replace("card-", "")
    if asin in direct_regions_map:
        card["data-direct-regions"] = direct_regions_map[asin]
        print(f"  • Card [{asin}]: data-direct-regions='{direct_regions_map[asin]}'")

index_file.write_text(str(soup), encoding="utf-8")
print("✅ Successfully updated index.html with data-direct-regions on all card wrappers!")
