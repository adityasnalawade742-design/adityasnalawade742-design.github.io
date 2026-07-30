import os
import sys
import json
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")

print("==================================================")
print("🔍 ADVANCED FEATURE & INTEGRITY AUDIT")
print("==================================================")

adv_findings = []

# 1. Price History Tracking
sync_script = repo_dir / "sync_exact_amazon_prices.py"
if sync_script.exists():
    content = sync_script.read_text(encoding="utf-8")
    if "price_history.json" not in content:
        adv_findings.append({
            "title": "📈 Price Drop History Tracking Missing",
            "desc": "Price sync updates current prices in real-time, but does not yet record historical price trends (price_history.json) to display '🔥 $X OFF (20% Price Drop)' badges on landing pages."
        })

# 2. Batch Pin Publisher Command
batch_pub = repo_dir / "publish_full_portfolio.py"
if not batch_pub.exists():
    adv_findings.append({
        "title": "📌 1-Click Full Portfolio Pin Publisher Command",
        "desc": "Individual product pin posting is supported, but a single CLI command (publish_full_portfolio.py) to publish/update Pinterest pins for all 9 products at once is missing."
    })

# 3. Accessibility & Keyboard Navigation (ARIA)
index_html = repo_dir / "index.html"
if index_html.exists():
    i_content = index_html.read_text(encoding="utf-8")
    if "aria-label" not in i_content:
        adv_findings.append({
            "title": "♿ Accessibility & Screen Reader (ARIA Tags)",
            "desc": "Interactive category chips and search clear buttons lack aria-label attributes for screen-reader accessibility."
        })

print(f"Found {len(adv_findings)} advanced feature opportunities:")
for idx, item in enumerate(adv_findings, 1):
    print(f"\n[{idx}] {item['title']}\n    {item['desc']}")

print("\n==================================================")
