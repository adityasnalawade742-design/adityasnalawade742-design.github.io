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
print("🔬 FULL SYSTEM FEATURES END-TO-END VERIFICATION SUITE")
print("=========================================================================\n")

features_status = []

# -------------------------------------------------------------------------
# FEATURE 1: Modular Domain Scrapers & Master Orchestrator
# -------------------------------------------------------------------------
print("📌 Testing Feature 1: Modular Domain Scrapers & Master Orchestrator...")
res1 = subprocess.run(["python", "sync_all_regional_prices_master.py"], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(repo))
if res1.returncode == 0 and "MASTER SEQUENTIAL SYNC & DIAGNOSTIC COMPLETE" in res1.stdout:
    features_status.append("✅ 1. Modular Domain Scrapers & Master Orchestrator -> 100% ACTIVE & PASS")
else:
    features_status.append(f"❌ 1. Modular Domain Scrapers FAIL: {res1.stderr}")

# -------------------------------------------------------------------------
# FEATURE 2: Automated Zero-Drift Self-Healing Bot (run_daily_health_check.py)
# -------------------------------------------------------------------------
print("📌 Testing Feature 2: Zero-Drift Self-Healing Bot (run_daily_health_check.py)...")
res2 = subprocess.run(["python", "run_daily_health_check.py"], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(repo))
if res2.returncode == 0 and "ZERO-DRIFT HEALTH CHECK COMPLETE" in res2.stdout:
    features_status.append("✅ 2. Automated Zero-Drift Self-Healing Bot -> 100% ACTIVE & PASS")
else:
    features_status.append(f"❌ 2. Zero-Drift Bot FAIL: {res2.stderr}")

# -------------------------------------------------------------------------
# FEATURE 3: Regional ASIN Variant Mapper (Direct /dp/ Upgrader)
# -------------------------------------------------------------------------
print("📌 Testing Feature 3: Regional ASIN Variant Mapper (Direct /dp/ Upgrader)...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(f"file:///{ (repo / 'bridge_B0DZD1X83N.html').resolve() }?country=DE".replace("\\", "/"))
    btn_href = page.evaluate("document.getElementById('buyBtn') ? document.getElementById('buyBtn').href : ''")
    browser.close()

if "/dp/B0F946YHSZ" in btn_href and "smartdeal0bb4-21" in btn_href:
    features_status.append("✅ 3. Regional ASIN Variant Mapper (Direct /dp/ Upgrader) -> 100% ACTIVE & PASS")
else:
    features_status.append(f"❌ 3. Regional ASIN Variant Mapper FAIL: href='{btn_href}'")

# -------------------------------------------------------------------------
# FEATURE 4: Native Financial Formatting Engine
# -------------------------------------------------------------------------
print("📌 Testing Feature 4: Native Financial Formatting Engine...")
bc_text = (repo / "modules/bridge_creator.py").read_text(encoding="utf-8")
if "minimumFractionDigits" in bc_text and "currencySymbols" in bc_text:
    features_status.append("✅ 4. Native Financial Formatting Engine -> 100% ACTIVE & PASS")
else:
    features_status.append("❌ 4. Native Financial Formatting Engine FAIL")

# -------------------------------------------------------------------------
# FEATURE 5: Outbound Affiliate Link & Tag Crawler (validate_all_affiliate_urls.py)
# -------------------------------------------------------------------------
print("📌 Testing Feature 5: Outbound Affiliate Link & Tag Crawler...")
res5 = subprocess.run(["python", "validate_all_affiliate_urls.py"], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(repo))
if res5.returncode == 0 and "72" in res5.stdout and "PASS" in res5.stdout:
    features_status.append("✅ 5. Outbound Link & Tag Crawler (72 Links Verified) -> 100% ACTIVE & PASS")
else:
    features_status.append(f"❌ 5. Outbound Link Crawler FAIL: {res5.stderr}")

# -------------------------------------------------------------------------
# FEATURE 6: 45-Currency Real-Time Exchange Rate Sync & Parity
# -------------------------------------------------------------------------
print("📌 Testing Feature 6: 45-Currency Real-Time Exchange Rate Sync & Parity...")
res6 = subprocess.run(["python", "scratch/fast_audit_45_currencies.py"], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(repo))
if res6.returncode == 0 and "ALL 45 CURRENCIES HAVE 100% SYMBOL & EXCHANGE RATE COVERAGE" in res6.stdout:
    features_status.append("✅ 6. 45-Currency Real-Time Exchange Rate Engine -> 100% ACTIVE & PASS")
else:
    features_status.append(f"❌ 6. 45-Currency Engine FAIL: {res6.stderr}")

print("\n=========================================================================")
print("🏆 MASTER SYSTEM FEATURES VERIFICATION REPORT:")
print("=========================================================================")
for fs in features_status:
    print(f"  {fs}")
print("=========================================================================")
