import json
from modules.seo_copywriter import generate_pin_seo_data
from post_all_10_homepage_pins import HOMEPAGE_PRODUCTS

out_lines = []
out_lines.append("=" * 80)
out_lines.append("📋 HIGH-REACH PINTEREST SEO COPYWRITING PREVIEW FOR ALL 10 HOMEPAGE PRODUCTS")
out_lines.append("=" * 80)

for idx, p in enumerate(HOMEPAGE_PRODUCTS, 1):
    seo = generate_pin_seo_data(p["title"])
    out_lines.append(f"\n[{idx}/10] ASIN: {p['asin']}")
    out_lines.append(f"📌 TITLE:       {seo['pin_title']}")
    out_lines.append(f"✍️ DESCRIPTION: {seo['description']}")
    out_lines.append("-" * 80)

with open("copy_preview_output.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))

print("Saved preview output to copy_preview_output.txt")
