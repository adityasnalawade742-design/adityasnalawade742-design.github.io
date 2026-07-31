import sys
import json
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")
reg_file = repo / "product_price_registry.json"

with open(reg_file, "r", encoding="utf-8") as f:
    reg = json.load(f)

clean_prices = {
    "B0DZD1X83N": "$20.00",
    "B0GYDXHF4G": "$35.00",
    "B0FXLYXM32": "$76.49",
    "B0C2YLN3H4": "$28.99",
    "B07HP22QTZ": "$12.99",
    "B0BZXNSW5K": "$19.99",
    "B0DXKGL1T2": "$38.57",
    "B0D1FRDFFX": "$35.98",
    "B0D8P8CSYP": "$18.99"
}

print("==================================================")
print("🛠️ CLEANING PRODUCT_PRICE_REGISTRY.JSON US PRICES")
print("==================================================")

for asin, price_str in clean_prices.items():
    if asin in reg:
        old_cp = reg[asin].get("current_price", "")
        old_us = reg[asin].get("regional_prices", {}).get("US", "")
        reg[asin]["current_price"] = price_str
        if "regional_prices" not in reg[asin]:
            reg[asin]["regional_prices"] = {}
        reg[asin]["regional_prices"]["US"] = price_str
        print(f" • [{asin:10s}]: Old CP='{old_cp:12s}' | Old US='{old_us:12s}' -> Clean='{price_str}'")

with open(reg_file, "w", encoding="utf-8") as f:
    json.dump(reg, f, indent=2, ensure_ascii=False)

print("\n==================================================")
print(" ✅ product_price_registry.json successfully cleaned!")
print("==================================================")
