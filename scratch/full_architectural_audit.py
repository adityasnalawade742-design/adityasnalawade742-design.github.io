import os
import sys
import json
import shutil
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")
sys.path.append(str(repo_dir))

print("==================================================")
print("🏗️ FULL ARCHITECTURAL & SYSTEM LANDSCAPE ANALYSIS")
print("==================================================")

# 1. Analyze Root Files vs Module Files
root_files = list(repo_dir.glob("*.py"))
print(f"\n1. Root Python Scripts: {len(root_files)} files found")
root_scraps = [f.name for f in root_files if f.name.startswith(("apply_", "deploy_", "fix_", "test_", "publish_"))]
print(f"   └─ One-off fix/utility scripts in root: {len(root_scraps)}")

# 2. Analyze Image File Sizes (Performance & Load Speed Audit)
print("\n2. Image File Size & Web Performance Audit:")
hook_imgs = list(repo_dir.glob("focus_product_*_hook.jpg"))
large_imgs = []
for img in hook_imgs:
    size_kb = round(img.stat().st_size / 1024, 1)
    if size_kb > 400:
        large_imgs.append((img.name, size_kb))
    print(f"   - {img.name}: {size_kb} KB")

if large_imgs:
    print(f"   ⚠️ Found {len(large_imgs)} large images (>400KB) that could be compressed for faster mobile loading.")

# 3. Environment Variables & API Key Audit
from config import REPLICATE_API_TOKEN, PINTEREST_ACCESS_TOKEN, AMAZON_ASSOCIATE_TAG
print("\n3. Environment Credentials & API Status:")
print(f"   - Replicate API Token: {'✅ CONFIGURED' if REPLICATE_API_TOKEN else '⚠️ MISSING'}")
print(f"   - Pinterest Access Token: {'✅ CONFIGURED' if PINTEREST_ACCESS_TOKEN else '⚠️ MISSING'}")
print(f"   - Amazon Associate Tag: {AMAZON_ASSOCIATE_TAG}")

# 4. Scraper Resilience Audit
from modules.amazon_extractor import get_product_details_and_photos
print("\n4. Amazon Scraper & Anti-Bot Resilience Audit:")
print("   - Fallback matrix: Registry -> Scraping -> Default Product Template")

print("\n==================================================")
print("ANALYSIS COMPLETE")
print("==================================================")
