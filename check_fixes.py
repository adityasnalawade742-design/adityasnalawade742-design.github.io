import re
import json
from pathlib import Path

repo = Path(__file__).resolve().parent
all_pass = True

def chk(name, condition, note=""):
    global all_pass
    status = "PASS" if condition else "FAIL"
    if not condition:
        all_pass = False
    tag = f" [{note}]" if note else ""
    print(f"  {'OK' if condition else 'XX'} [{status}] {name}{tag}")
    return condition

print("\n=== 1. modules/bridge_creator.py ===")
bc = (repo / "modules/bridge_creator.py").read_text(encoding="utf-8")
chk("C1 - No hardcoded G:/CLI absolute paths", len(re.findall(r'Path\("G:/CLI', bc)) == 0)
chk("C1b - _MODULE_DIR defined", "_MODULE_DIR = Path(__file__).resolve().parent.parent" in bc)
chk("C2 - Static ?v=3 removed", "?v=3" not in bc)
chk("C2b - int(time.time()) used", "int(time.time())" in bc)
chk("C3 - Raw images guarded with Path.exists()", "Path(img_path).exists()" in bc)
chk("H3 - product=dict(product_data)", "product=dict(product_data)" in bc)
chk("NL5 - Dynamic rating-count in template", "product.reviews or '1,200'" in bc)
chk("M3 - Hardcoded lamp copy removed", "Nightstand Declutter:" not in bc)
chk("M3b - Dynamic editorial features", "seo.description or product.description" in bc)

print("\n=== 2. web_console_server.py ===")
wcs = (repo / "web_console_server.py").read_text(encoding="utf-8")
chk("NM2 - item NameError fixed (uses data.get('title'))", "title=data.get('title', title)" in wcs)
chk("NM3 - n8n webhook default URL fixed to /webhook/pinterest-batch", "/webhook/pinterest-batch" in wcs)
chk("NL4 - Empty body guard in handle_api_delete_homepage_product", "content_length > 0 else {}" in wcs)

print("\n=== 3. daily_price_updater.py ===")
dpu = (repo / "daily_price_updater.py").read_text(encoding="utf-8")
chk("NH1 - Safe url access with data.get('url', '')", "data.get(\"url\", \"\")" in dpu or 'data.get("url", "")' in dpu)
chk("NH2 - os.system replaced with subprocess.run(..., cwd=str(BASE_DIR))", "os.system('git" not in dpu)
chk("NM4 - Hardcoded pattern_img regex replacement removed", "pattern_img" not in dpu)
chk("NM5 - Retired ASINs removed from DEFAULT_REGISTRY", "B0BDRSG2BT" not in dpu and "B0GGHJ1J4L" not in dpu)

print("\n=== 4. modules/pinterest_publisher.py ===")
pp = (repo / "modules/pinterest_publisher.py").read_text(encoding="utf-8")
chk("NL1 - Exception returns API_ERROR dict in publish_pin_to_pinterest", 'return {"status": "API_ERROR", "error": str(e)' in pp)

print("\n=== 5. run_daily_health_check.py ===")
hc = (repo / "run_daily_health_check.py").read_text(encoding="utf-8")
chk("H1 - try/except ValueError on float(base_usd)", "except ValueError:" in hc)
chk("H2 - pt.get_text(strip=True)", "pt.get_text(strip=True)" in hc)
chk("NL2 - File existence guard before reading", "if not registry_file.exists() or not index_file.exists():" in hc)

print("\n=== 6. sync_exact_amazon_prices.py ===")
se = (repo / "sync_exact_amazon_prices.py").read_text(encoding="utf-8")
chk("NL3 - Registry file existence guard present", "if not registry_path.exists():" in se)
chk("NL3b - Git commit check=False", "check=False" in se)

print("\n=== 7. modules/scrapers/scrape_us.py ===")
su = (repo / "modules/scrapers/scrape_us.py").read_text(encoding="utf-8")
chk("NM1 - Non-silent exception handler", "print(f\"  ⚠️ Scrape page error for {asin}: {e}\")" in su)

print()
print("=" * 60)
if all_pass:
    print("ALL PASS-1 AND PASS-2 FIXES VERIFIED - 100% PASS!")
else:
    print("SOME FIXES FAILED VERIFICATION - SEE XX ITEMS ABOVE")
print("=" * 60)
