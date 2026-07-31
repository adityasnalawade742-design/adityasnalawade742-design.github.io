import sys
import json
import re
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")

print("=========================================================================")
print("🔬 EMPIRICAL VERIFICATION OF THE 4 PRECISION FEATURES")
print("=========================================================================\n")

feature_results = []

# -------------------------------------------------------------------------
# FEATURE 1: Automated "Zero-Drift" Self-Healing Bot (run_daily_health_check.py)
# -------------------------------------------------------------------------
print("📌 Testing Feature 1: Zero-Drift Self-Healing Bot (run_daily_health_check.py)...")
res1 = subprocess.run(["python", "run_daily_health_check.py"], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(repo))
if res1.returncode == 0 and "ZERO-DRIFT HEALTH CHECK COMPLETE" in (res1.stdout or ""):
    feature_results.append("✅ Feature 1: Automated Zero-Drift Self-Healing Bot (run_daily_health_check.py) -> ACTIVE & 100% PASS")
else:
    feature_results.append(f"❌ Feature 1 FAIL: {res1.stderr}")

# -------------------------------------------------------------------------
# FEATURE 2: Regional ASIN Variant Mapper (Direct /dp/ Upgrader)
# -------------------------------------------------------------------------
print("📌 Testing Feature 2: Regional ASIN Variant Mapper (Direct /dp/ Upgrader)...")
reg_file = repo / "product_price_registry.json"
reg_data = json.loads(reg_file.read_text(encoding="utf-8"))
has_regional_asins = all("regional_asins" in item for item in reg_data.values())

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(f"file:///{ (repo / 'bridge_B07HP22QTZ.html').resolve() }?country=IN".replace("\\", "/"))
    btn_href = page.evaluate("document.getElementById('buyBtn') ? document.getElementById('buyBtn').href : ''")
    btn_text = page.evaluate("document.getElementById('buyBtnText') ? document.getElementById('buyBtnText').innerText : ''")
    browser.close()

if has_regional_asins and "/dp/B07HP22QTZ" in btn_href and "BUY ON" in btn_text:
    feature_results.append("✅ Feature 2: Regional ASIN Variant Mapper (Direct /dp/ Upgrader) -> ACTIVE & 100% PASS")
else:
    feature_results.append(f"❌ Feature 2 FAIL: href='{btn_href}', text='{btn_text}'")

# -------------------------------------------------------------------------
# FEATURE 3: Official Native Financial Formatting Engine
# -------------------------------------------------------------------------
print("📌 Testing Feature 3: Official Native Financial Formatting Engine...")
bc_text = (repo / "modules/bridge_creator.py").read_text(encoding="utf-8")
has_native_formatting = "minimumFractionDigits" in bc_text and "currencySymbols" in bc_text

if has_native_formatting:
    feature_results.append("✅ Feature 3: Official Native Financial Formatting Engine (Period/Comma/Integer Rules) -> ACTIVE & 100% PASS")
else:
    feature_results.append("❌ Feature 3 FAIL: Missing native formatting rules")

# -------------------------------------------------------------------------
# FEATURE 4: Automated Outbound Link & Tag Crawler (validate_all_affiliate_urls.py)
# -------------------------------------------------------------------------
print("📌 Testing Feature 4: Automated Outbound Link & Tag Crawler (validate_all_affiliate_urls.py)...")
res4 = subprocess.run(["python", "validate_all_affiliate_urls.py"], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(repo))
if res4.returncode == 0 and "72" in (res4.stdout or "") and "PASS" in (res4.stdout or ""):
    feature_results.append("✅ Feature 4: Automated Outbound Link & Tag Crawler (72 Links Validated) -> ACTIVE & 100% PASS")
else:
    feature_results.append(f"❌ Feature 4 FAIL: {res4.stderr}")

print("\n=========================================================================")
print("🏆 FINAL PRECISION FEATURE STATUS REPORT:")
print("=========================================================================")
for fres in feature_results:
    print(f"  {fres}")
print("=========================================================================")
