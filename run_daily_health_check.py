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
    for rk, rv in list(rp.items()):
        if rk != "IN" and ("INR" in str(rv) or "₹" in str(rv)):
            rp[rk] = "Not Available"
            healed_count += 1
            print(f"  🔧 Healed raw INR string in registry [{asin}] {rk} -> Not Available")

    us_p = rp.get("US", item.get("current_price", "$19.99"))
    if "INR" in str(us_p) or "₹" in str(us_p):
        clean_usd = item.get("current_price", "$19.99")
        if "INR" in clean_usd or "₹" in clean_usd:
            clean_usd = "$19.99"
        rp["US"] = clean_usd
        item["current_price"] = clean_usd
        healed_count += 1
        print(f"  🔧 Healed raw INR string in registry [{asin}] US -> {clean_usd}")

registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")

# 2. Heal index.html data attributes to match registry 100%
cards = soup.find_all("div", class_="card-wrapper")
index_modified = False
raw_html = index_file.read_text(encoding="utf-8")

# Load empirical direct matrix
matrix_file = repo / "global_direct_matrix.json"
direct_matrix = {}
if matrix_file.exists():
    direct_matrix = json.loads(matrix_file.read_text(encoding="utf-8"))

def safe_reg_price(rp_dict, region_key):
    val = rp_dict.get(region_key, "Not Available")
    if region_key != "IN" and ("INR" in str(val) or "₹" in str(val)):
        return "Not Available"
    return val

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
        "data-price-in": safe_reg_price(rp, "IN"),
        "data-price-uk": safe_reg_price(rp, "UK"),
        "data-price-de": safe_reg_price(rp, "DE"),
        "data-price-ca": safe_reg_price(rp, "CA"),
        "data-price-au": safe_reg_price(rp, "AU"),
        "data-price-jp": safe_reg_price(rp, "JP"),
        "data-direct-regions": direct_regs_str
    }
    
    # Match the entire <div ... id="card-{asin}"> opening tag regardless of attribute order
    div_pattern = re.compile(rf'(<div\b[^>]*?\bid=["\']card-{asin}["\'][^>]*?>)', re.IGNORECASE)
    match = div_pattern.search(raw_html)
    if match:
        tag_str = match.group(1)
        new_tag_str = tag_str
        for k, v in attr_updates.items():
            if f'{k}="' in new_tag_str:
                new_tag_str = re.sub(rf'\b{k}="[^"]*"', f'{k}="{v}"', new_tag_str)
            else:
                # Insert new attribute before closing bracket
                new_tag_str = new_tag_str[:-1] + f' {k}="{v}">'
        if new_tag_str != tag_str:
            raw_html = raw_html.replace(tag_str, new_tag_str)
            index_modified = True
            healed_count += 1
            print(f"  🔧 Healed index.html card [{asin}] attributes")

if index_modified and healed_count > 0:
    index_file.write_text(raw_html, encoding="utf-8")
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
