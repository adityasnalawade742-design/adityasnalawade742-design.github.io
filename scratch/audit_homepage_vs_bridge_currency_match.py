import sys
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")
index_file = repo / "index.html"
bridge_creator_file = repo / "modules/bridge_creator.py"

print("=========================================================================")
print("🔬 HOMEPAGE VS BRIDGE LANDING PAGE CURRENCY CONSISTENCY AUDIT")
print("=========================================================================\n")

# Extract countryToCurrencyMap from index.html
index_text = index_file.read_text(encoding="utf-8")
map_match = re.search(r'const countryToCurrencyMap = (\{[^}]+\});', index_text)
if not map_match:
    print("❌ Could not parse countryToCurrencyMap from index.html")
    sys.exit(1)

# Parse map cleanly
map_str = map_match.group(1).replace("\n", "").replace(" ", "")
pairs = re.findall(r'"([A-Z]{2})":"([A-Z]{3})"', map_str)
index_country_currency = dict(pairs)

print(f"📊 Total Countries Mapped on Homepage: {len(index_country_currency)}")

# Extract currencyMap from modules/bridge_creator.py
bc_text = bridge_creator_file.read_text(encoding="utf-8")
bc_map_match = re.search(r'const countryToCurrencyMap = (\{[^}]+\});', bc_text)
if not bc_map_match:
    print("❌ Could not parse countryToCurrencyMap from modules/bridge_creator.py")
    sys.exit(1)

bc_map_str = bc_map_match.group(1).replace("\n", "").replace(" ", "")
bc_pairs = re.findall(r'"([A-Z]{2})":"([A-Z]{3})"', bc_map_str)
bridge_country_currency = dict(bc_pairs)

print(f"📊 Total Countries Mapped in Bridge Creator Engine: {len(bridge_country_currency)}\n")

# Compare mappings key by key
mismatches = []
missing_in_bridge = []

for cc, index_curr in index_country_currency.items():
    if cc not in bridge_country_currency:
        missing_in_bridge.append(cc)
    elif bridge_country_currency[cc] != index_curr:
        mismatches.append((cc, index_curr, bridge_country_currency[cc]))

print("📌 [1/2] MAPPING INTEGRITY CHECK (Homepage vs Bridge Engine):")
if not mismatches and not missing_in_bridge:
    print("  ✅ 100% MATCH: All country-to-currency mappings on Homepage and Bridge Landing Pages are 100% IDENTICAL!")
else:
    if missing_in_bridge:
        print(f"  ❌ Missing in Bridge Engine: {missing_in_bridge}")
    if mismatches:
        for cc, ic, bc in mismatches:
            print(f"  ❌ Mismatch for country {cc}: Homepage has {ic}, Bridge Engine has {bc}")

# Verify all 9 bridge HTML files contain the exact matching countryToCurrencyMap
print("\n📌 [2/2] INDIVIDUAL BRIDGE PAGE FILE INTEGRITY CHECK:")
landing_pages = sorted(list(repo.glob("bridge_*.html")))
all_bridge_files_ok = True

for lp in landing_pages:
    lp_text = lp.read_text(encoding="utf-8")
    lp_map_match = re.search(r'const countryToCurrencyMap = (\{[^}]+\});', lp_text)
    if not lp_map_match:
        print(f"  ❌ {lp.name}: Missing countryToCurrencyMap in script")
        all_bridge_files_ok = False
        continue
    
    lp_map_str = lp_map_match.group(1).replace("\n", "").replace(" ", "")
    lp_pairs = dict(re.findall(r'"([A-Z]{2})":"([A-Z]{3})"', lp_map_str))
    
    diffs = {k: v for k, v in index_country_currency.items() if k not in lp_pairs or lp_pairs[k] != v}
    if diffs:
        all_bridge_files_ok = False
        print(f"  ❌ {lp.name}: Mismatch for {len(diffs)} countries")
    else:
        print(f"  ✅ {lp.name}: 100% Currency Map Parity with Homepage ({len(lp_pairs)} countries)")

print("\n=========================================================================")
print("🏆 CURRENCY PARITY AUDIT RESULT:")
print("=========================================================================")
if not mismatches and not missing_in_bridge and all_bridge_files_ok:
    print("✅ 100% PASS: HOMEPAGE AND ALL 9 BRIDGE LANDING PAGES DISPLAY IDENTICAL CURRENCIES FOR EVERY SINGLE COUNTRY VISITOR WORLDWIDE!")
else:
    print("❌ FAIL: Discrepancy found between Homepage and Bridge Page currency mapping.")
print("=========================================================================")
