import os
import sys
import json
import re
from pathlib import Path

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

print("==================================================")
print("EXECUTING DEEP SYSTEM AUDIT ACROSS ALL MODULES")
print("==================================================")

issues = []

# 1. Audit Affiliate Tag across all landing pages
bridge_files = list(repo_dir.glob("bridge_*.html"))
print(f"1. Auditing {len(bridge_files)} landing pages for Amazon affiliate tag smartdeal0358-21...")
for bf in bridge_files:
    content = bf.read_text(encoding="utf-8")
    if "smartdeal0358-21" not in content:
        issues.append(f"Landing page {bf.name} is missing Amazon affiliate tag 'smartdeal0358-21'!")

# 2. Audit Image paths referenced in bridge pages
print("2. Auditing image references in landing pages...")
for bf in bridge_files:
    content = bf.read_text(encoding="utf-8")
    img_matches = re.findall(r'src=["\'](\./focus_product_[^"\']+)["\']', content)
    for img_path in img_matches:
        clean_img = img_path.split('?')[0].replace('./', '')
        full_img = repo_dir / clean_img
        if not full_img.exists():
            issues.append(f"Landing page {bf.name} references missing image file: {clean_img}")

# 3. Audit product_price_registry.json
reg_path = repo_dir / "product_price_registry.json"
print("3. Auditing product_price_registry.json schema & ASIN integrity...")
if reg_path.exists():
    try:
        reg = json.loads(reg_path.read_text(encoding="utf-8"))
        for asin, item in reg.items():
            if not item.get("title"):
                issues.append(f"Registry entry {asin} missing 'title'!")
            if not item.get("current_price"):
                issues.append(f"Registry entry {asin} missing 'current_price'!")
            if not item.get("hook_image"):
                issues.append(f"Registry entry {asin} missing 'hook_image'!")
            hook_file = repo_dir / item.get("hook_image", "")
            if not hook_file.exists():
                issues.append(f"Registry entry {asin} references missing hook image: {item.get('hook_image')}")
    except Exception as e:
        issues.append(f"Failed parsing product_price_registry.json: {e}")

# 4. Audit global_tag_defaults.json
g_path = repo_dir / "global_tag_defaults.json"
print("4. Auditing global_tag_defaults.json...")
if g_path.exists():
    try:
        g_def = json.loads(g_path.read_text(encoding="utf-8"))
        required_keys = ["tag_width", "tag_rotation", "tag_pos_x", "tag_pos_y"]
        for k in required_keys:
            if k not in g_def:
                issues.append(f"global_tag_defaults.json missing required key '{k}'!")
    except Exception as e:
        issues.append(f"Failed parsing global_tag_defaults.json: {e}")

print("\n==================================================")
if issues:
    print(f"⚠️ FOUND {len(issues)} ISSUES DURING DEEP AUDIT:")
    for idx, iss in enumerate(issues, 1):
        print(f"  [{idx}] {iss}")
else:
    print("✅ 100% CLEAN DEEP AUDIT: Zero missing files, zero affiliate link breaks, zero schema errors!")
print("==================================================")
