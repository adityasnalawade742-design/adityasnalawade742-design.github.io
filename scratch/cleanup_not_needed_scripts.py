import sys
import shutil
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")
scratch_dir = repo / "scratch"
archive_dir = scratch_dir / "archive_legacy_scripts"

# Useful diagnostic tools to keep in scratch/
keep_in_scratch = {
    "master_zero_404_audit.py",
    "check_all_products_live.py",
    "rebuild_all_price_badges_usd.py",
    "render_bird_lamp.py",
    "test_live_amazon_404.py",
    "test_variant_checker.py",
    "audit_index_prices.py",
    "sync_index_html_clean.py",
    "verify_4_master_bots.py",
    "find_recent_images.py",
    "check_bird_mtime.py",
    "inspect_bird_images.py",
    "count_py_files.py",
    "cleanup_not_needed_scripts.py"
}

deleted_count = 0

print("==================================================")
print("🧹 CLEANING UP NOT-NEEDED & LEGACY SCRATCH FILES")
print("==================================================")

# 1. Delete archive_legacy_scripts directory if exists
if archive_dir.exists():
    arch_files = list(archive_dir.glob("*"))
    shutil.rmtree(archive_dir)
    deleted_count += len(arch_files)
    print(f" • Removed directory: scratch/archive_legacy_scripts/ ({len(arch_files)} files deleted)")

# 2. Delete one-off testing scripts in scratch/
if scratch_dir.exists():
    for item in list(scratch_dir.glob("*")):
        if item.is_file():
            if item.name not in keep_in_scratch:
                item.unlink()
                deleted_count += 1
                print(f" • Deleted legacy scratch file: scratch/{item.name}")

print("\n==================================================")
print(f" ✅ CLEANUP COMPLETE: Deleted {deleted_count} not-needed files!")
print("==================================================")
