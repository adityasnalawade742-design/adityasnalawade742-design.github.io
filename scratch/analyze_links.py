import re
import json
import urllib.parse
import sys
from pathlib import Path

import sys
sys.path.append("G:/CLI/pinterest-auto-affiliate")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from modules.amazon_extractor import extract_asin_from_url, get_product_details_and_photos

links_file = Path("amazon_products_links.txt")
lines = [l.strip() for l in links_file.read_text(encoding="utf-8").splitlines() if l.strip()]

results = []
print(f"🔍 Analyzing {len(lines)} Amazon Links from amazon_products_links.txt...\n")

for idx, url in enumerate(lines, 1):
    asin = extract_asin_from_url(url)
    slug_match = re.search(r'amazon\.[a-z.]+/([^/]+)/dp/', url)
    slug = slug_match.group(1).replace('-', ' ') if slug_match else ""
    
    cv_ct = re.search(r'cv_ct_cx=([^&]+)', url)
    search_hint = urllib.parse.unquote(cv_ct.group(1)).replace('+', ' ') if cv_ct else ""
    
    results.append({
        "index": idx,
        "asin": asin,
        "slug": slug,
        "search_hint": search_hint,
        "url": url
    })

print(f"{'#':<3} | {'ASIN':<10} | {'SLUG / TITLE HINT':<45} | {'SEARCH HINT':<35}")
print("-" * 100)
for r in results:
    hint = r["slug"] or r["search_hint"] or "Direct ASIN Link"
    print(f"{r['index']:<3} | {r['asin']:<10} | {hint[:45]:<45} | {r['search_hint'][:35]:<35}")

# Save json analysis to scratch
scratch_dir = Path("G:/CLI/pinterest-auto-affiliate/scratch")
scratch_dir.mkdir(parents=True, exist_ok=True)
with open(scratch_dir / "analyzed_links.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
