import os
import sys
import shutil
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")
archive_dir = repo_dir / "scratch" / "archive_legacy_scripts"
archive_dir.mkdir(parents=True, exist_ok=True)

print("==================================================")
print("🧹 STEP 2: ORGANIZING ROOT REPOSITORY DIRECTORY")
print("==================================================")

# Legacy fix/utility scripts to archive
legacy_scripts = [
    "apply_user_custom_image_b9e65.py",
    "apply_user_photo_fix.py",
    "apply_photo_1_B0BZXNSW5K.py",
    "deploy_instant_filename_fix.py",
    "publish_flux_B0BZXNSW5K.py",
    "fix_render.py",
    "find_100pct_active_asins.py",
    "find_100pct_new_openable_home_decor.py",
    "find_different_niche_home_decor.py",
    "find_fresh_live_serpapi_products.py",
    "find_fresh_verified_amazon_products.py",
    "find_working_products.py",
    "fetch_adult_home_decor_products.py",
    "fetch_verified_lifestyle_home_decor.py",
    "fast_audit_9_storefronts.py",
    "fast_audit_all_urls.py",
    "audit_ALL_global_amazon_stores.py",
    "audit_all_amazon_urls_404.py"
]

moved_count = 0
for script in legacy_scripts:
    src_file = repo_dir / script
    if src_file.exists():
        dst_file = archive_dir / script
        shutil.move(str(src_file), str(dst_file))
        moved_count += 1
        print(f" 📂 Archived: {script} ➔ scratch/archive_legacy_scripts/")

print("\n--------------------------------------------------")
print(f"🎉 CLEANUP COMPLETE: Archived {moved_count} legacy scripts out of root directory!")
print("==================================================")
