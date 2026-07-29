import sys
import json
from pathlib import Path

sys.path.append("G:/CLI/pinterest-auto-affiliate")

from modules.amazon_finder import fetch_amazon_products

queries = [
    ("Ambient & Sculptural Lighting", "flame aroma diffuser warm amber glow"),
    ("Ceramic & Stoneware Vases", "white ceramic donut vase pampas grass set"),
    ("Tabletop Sculptures & Objects", "abstract thinker statue bookshelf decor"),
    ("Architectural Mirrors & Wall Decor", "wavy vanity wall mirror cream frame"),
    ("Cozy Tactile Textiles & Throws", "chunky knit throw blanket soft cozy"),
    ("Framed Minimalist Wall Art", "framed neutral botanical print set black frame"),
    ("Natural Woven Storage & Baskets", "water hyacinth storage basket set natural")
]

selected_portfolio = {}

for category_name, query_str in queries:
    print(f"\n🔍 Searching live Amazon products for category: [{category_name}] ('{query_str}')...")
    items = fetch_amazon_products(query=query_str, num_results=2, min_price=10.0, max_price=65.0)
    selected_portfolio[category_name] = items

scratch_dir = Path("G:/CLI/pinterest-auto-affiliate/scratch")
scratch_dir.mkdir(parents=True, exist_ok=True)
with open(scratch_dir / "example_selected_archetypes.json", "w", encoding="utf-8") as f:
    json.dump(selected_portfolio, f, indent=2)

print("\nSaved example selections to scratch/example_selected_archetypes.json!")
