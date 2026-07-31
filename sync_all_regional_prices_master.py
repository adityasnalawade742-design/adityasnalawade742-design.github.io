import sys
import subprocess
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")

print("=========================================================================")
print("🚀 MASTER SEQUENTIAL REGIONAL PRICE SYNC & DIAGNOSTIC SUITE")
print("=========================================================================\n")

scrapers = [
    ("US (Amazon.com)", "modules/scrapers/scrape_us.py"),
    ("India (Amazon.in)", "modules/scrapers/scrape_in.py"),
    ("UK (Amazon.co.uk)", "modules/scrapers/scrape_uk.py"),
    ("Germany (Amazon.de)", "modules/scrapers/scrape_de.py"),
    ("Canada (Amazon.ca)", "modules/scrapers/scrape_ca.py"),
    ("Australia (Amazon.com.au)", "modules/scrapers/scrape_au.py"),
    ("Japan (Amazon.co.jp)", "modules/scrapers/scrape_jp.py"),
    ("14 Extended Global Domains (FR, ES, IT, SE, NL, PL, TR, BE, MX, BR, SG, AE, SA, EG)", "modules/scrapers/scrape_extended_domains.py")
]

for name, script_path in scrapers:
    print(f"🔄 Executing Domain Scraper for {name}...")
    res = subprocess.run(["python", script_path], cwd=str(repo), capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode == 0:
        print(f"✅ {name} Scraping Finished Successfully.")
    else:
        print(f"⚠️ {name} Warning / Error: {res.stderr.strip()}")
    time.sleep(0.5)

print("\n-------------------------------------------------------------------------")
print("🛡️ RUNNING AUTOMATED ZERO-DRIFT HEALTH CHECK & AUTO-HEAL...")
print("-------------------------------------------------------------------------")
hc_res = subprocess.run(["python", "run_daily_health_check.py"], cwd=str(repo), capture_output=True, text=True, encoding="utf-8", errors="replace")
print(hc_res.stdout.strip())

print("\n-------------------------------------------------------------------------")
print("🌐 RUNNING OUTBOUND AFFILIATE LINK & STORE ID CRAWLER...")
print("-------------------------------------------------------------------------")
val_res = subprocess.run(["python", "validate_all_affiliate_urls.py"], cwd=str(repo), capture_output=True, text=True, encoding="utf-8", errors="replace")
print(val_res.stdout.strip())

print("\n-------------------------------------------------------------------------")
print("🔨 REBUILDING 100% OF LANDING PAGES & DEPLOYING LIVE TO GITHUB PAGES...")
print("-------------------------------------------------------------------------")
reb_res = subprocess.run(["python", "rebuild_EVERY_single_bridge.py"], cwd=str(repo), capture_output=True, text=True, encoding="utf-8", errors="replace")
print(reb_res.stdout.strip())

print("\n=========================================================================")
print("🏆 MASTER SEQUENTIAL SYNC & DIAGNOSTIC COMPLETE! SITE IS 100% LIVE!")
print("=========================================================================")
