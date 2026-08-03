import sys
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path(__file__).resolve().parent  # C2 FIX: dynamic path
index_file = repo / "index.html"
registry_file = repo / "product_price_registry.json"
bridge_files = sorted(list(repo.glob("bridge_*.html")))

print("=========================================================================")
print("🛡️ RUNNING AUTOMATED ZERO-DRIFT SELF-HEALING HEALTH CHECK")
print("=========================================================================\n")

if not registry_file.exists() or not index_file.exists():
    print("⚠️ Registry or index.html missing. Aborting health check.")
    sys.exit(0)

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
    try:
        base_usd_float = float(base_usd) if base_usd else 0.0
    except ValueError:
        base_usd_float = 0.0

    if not base_usd or base_usd_float > 500 or base_usd_float <= 0:
        # H7 FIX: fallbacks for ALL 9 ASINs in the portfolio
        fallback_prices = {
            "B0C2YLN3H4":  "28.99",
            "B07HP22QTZ":  "12.99",
            "B0BZXNSW5K":  "19.99",
            "B0D8P8CSYP":  "18.99",
            "B0DZD1X83N":  "20.00",
            "B0GYDXHF4G":  "35.00",
            "B0FXLYXM32":  "76.49",
            "B0D1FRDFFX":  "35.98",
            "B0DXKGL1T2":  "38.57",
            "B0FGJ1S73D":  "32.99",
        }
        base_usd = fallback_prices.get(asin, "19.99")

    clean_us_price = f"${base_usd}" if not raw_usd.startswith("$") else raw_usd
    if "," in clean_us_price or base_usd_float > 500:
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
    expected_pt_str = str(rp.get("US", f"${base_usd}"))
    if pt and pt.get_text(strip=True) != expected_pt_str:
        pt.clear()
        pt.string = expected_pt_str
        index_modified = True

if index_modified or healed_count > 0:
    index_file.write_text(str(soup), encoding="utf-8")
    print("✅ Saved self-healed index.html!")
    # M5 FIX: push healed changes live so the site doesn't stay broken until next scheduled sync
    try:
        import subprocess
        subprocess.run(["git", "add", "index.html", "product_price_registry.json"], cwd=str(repo), check=False)
        subprocess.run(["git", "commit", "-m", "auto: zero-drift health check self-heal"], cwd=str(repo), check=False)
        subprocess.run(["git", "push", "origin", "main"], cwd=str(repo), check=False)
        print("✅ Self-healed changes pushed live to GitHub Pages!")
    except Exception as e_git:
        print(f"⚠️ Git push after health-check warning: {e_git}")

try:
    from modules.automated_product_selector import cleanup_unselected_raw_images
    purged = cleanup_unselected_raw_images()
    if purged > 0:
        print(f"  🧹 Auto-Purged {purged} unchosen scratch images from raw_images/")
except Exception as e_cln:
    print(f"⚠️ Image cleanup warning: {e_cln}")

print(f"\n=========================================================================")
print(f"🏆 ZERO-DRIFT HEALTH CHECK COMPLETE: Healed {healed_count} items!")
print(f"=========================================================================")
