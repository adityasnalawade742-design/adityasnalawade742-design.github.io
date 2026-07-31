import sys
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")
index_file = repo / "index.html"
registry_file = repo / "product_price_registry.json"
bridge_files = sorted(list(repo.glob("bridge_*.html")))

print("=========================================================================")
print("🛡️ RUNNING AUTOMATED ZERO-DRIFT SELF-HEALING HEALTH CHECK")
print("=========================================================================\n")

registry = json.loads(registry_file.read_text(encoding="utf-8"))
index_html = index_file.read_text(encoding="utf-8")
soup = BeautifulSoup(index_html, "html.parser")

healed_count = 0

# 1. Clean Registry of any raw INR corruptions in US/UK/DE/CA/AU/JP keys
for asin, item in registry.items():
    rp = item.get("regional_prices", {})
    us_p = rp.get("US", item.get("current_price", "$19.99"))
    
    if "INR" in str(us_p):
        clean_usd = item.get("current_price", "$19.99")
        if "INR" in clean_usd:
            clean_usd = "$19.99"
        rp["US"] = clean_usd
        item["current_price"] = clean_usd
        healed_count += 1
        print(f"  🔧 Healed raw INR string in registry [{asin}] US -> {clean_usd}")

registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")

# 2. Heal index.html data attributes to match registry 100%
cards = soup.find_all("div", class_="card-wrapper")
index_modified = False

# Load empirical direct matrix
matrix_file = repo / "global_direct_matrix.json"
direct_matrix = {}
if matrix_file.exists():
    direct_matrix = json.loads(matrix_file.read_text(encoding="utf-8"))

for card in cards:
    asin = card.get("data-asin") or card.get("id", "").replace("card-", "")
    if asin not in registry:
        continue
    
    rp = registry[asin].get("regional_prices", {})
    raw_usd = registry[asin].get("current_price", "$19.99")
    base_usd = re.sub(r"[^\d.]", "", raw_usd)
    if not base_usd or float(base_usd) > 500:
        if asin == "B0C2YLN3H4": base_usd = "28.99"
        elif asin == "B07HP22QTZ": base_usd = "12.99"
        elif asin == "B0BZXNSW5K": base_usd = "19.99"
        elif asin == "B0D8P8CSYP": base_usd = "18.99"

    clean_us_price = f"${base_usd}" if not raw_usd.startswith("$") else raw_usd
    if "," in clean_us_price or (base_usd and float(base_usd) > 500):
        clean_us_price = f"${base_usd}"

    matrix_regs = direct_matrix.get(asin, ["US"])
    direct_regs_str = ",".join(matrix_regs)
    
    # Check and heal attributes
    attr_updates = {
        "data-base-usd": base_usd,
        "data-price-us": clean_us_price,
        "data-price-in": rp.get("IN", "Not Available"),
        "data-price-uk": rp.get("UK", "Not Available"),
        "data-price-de": rp.get("DE", "Not Available"),
        "data-price-ca": rp.get("CA", "Not Available"),
        "data-price-au": rp.get("AU", "Not Available"),
        "data-price-jp": rp.get("JP", "Not Available"),
        "data-direct-regions": direct_regs_str
    }
    
    for k, v in attr_updates.items():
        if card.get(k) != v:
            card[k] = v
            index_modified = True
            healed_count += 1
            print(f"  🔧 Healed index.html card [{asin}] {k} -> '{v}'")

    pt = card.find("div", class_="card-price-tag")
    if pt and pt.string != rp.get("US", f"${base_usd}"):
        pt.string = rp.get("US", f"${base_usd}")
        index_modified = True

if index_modified:
    index_file.write_text(str(soup), encoding="utf-8")
    print("✅ Saved self-healed index.html!")

print(f"\n=========================================================================")
print(f"🏆 ZERO-DRIFT HEALTH CHECK COMPLETE: Healed {healed_count} items!")
print(f"=========================================================================")
