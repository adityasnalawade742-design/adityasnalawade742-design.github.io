import os
import sys
import shutil
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")
archive_dir = repo_dir / "scratch" / "archive_legacy_scripts"
archive_dir.mkdir(parents=True, exist_ok=True)

# Files to move to archive
legacy_files = [
    "apply_user_sunset_image_acjw3.py", "auto_process_next.py", "check_all_notice_boxes.py",
    "check_exact_asin_urls.py", "create_board.py", "direct_insert_wavy_mirror.py",
    "extract_mushroom.py", "extract_sunset.py", "fetch_boards.py", "find_globally_openable_asins.py",
    "find_unique_pinterest_trends.py", "find_white_bg_products.py", "fix_sunset_lamp_headline.py",
    "generate_new_product_links.py", "get_adult_decor_direct.py", "get_different_home_decor_direct.py",
    "get_lifestyle_products_fast.py", "get_real_white_bg_amazon_products.py", "process_bird_lamp_run.py",
    "process_crackle_flame_diffuser.py", "process_home_decor_product.py", "process_mushroom_lamp.py",
    "process_new_link.py", "process_new_product.py", "process_nextmug.py", "process_selected_bedside_lamp.py",
    "process_selected_crystal_suncatcher.py", "process_selected_sunset_lamp.py", "process_single_wavy_mirror.py",
    "process_tapestry_product.py", "process_terrarium_product.py", "process_test_lamp.py",
    "process_true_single_scene_donut_vases.py", "process_user_product.py", "process_vintage_lamp.py",
    "process_wavy_mirror.py", "publish_flux_B0D1FRDFFX.py", "publish_flux_B0DZD1X83N.py",
    "publish_mushroom_fast.py", "publish_sunset_fast.py", "regenerate_bridge.py", "render_b0dx.py",
    "render_cream_theme.py", "render_floating_graphic.py", "render_perfect_template.py",
    "run_custom_luxury_prompt.py", "run_single_product.py", "run_sunset_lamp.py", "search_live_amazon_niche.py",
    "test_all_live_links_click.py", "test_batch_products.py", "test_cozy_vibe_scorer.py",
    "test_donut_vase_all_countries.py", "test_easyocr.py", "test_fast_detector.py", "test_gemini_ocr.py",
    "test_geo_feature_verification.py", "test_geo_redirect_logic.py", "test_img2img_replicate.py",
    "test_lifestyle_detector.py", "test_live_github_pages_urls.py", "test_live_pin_publish.py",
    "test_new_products.py", "test_playwright_geo_links.py", "test_scrape_links.py", "test_text_detector.py",
    "update_B0BZXNSW5K_image.py", "verify_new_asins.py"
]

moved_count = 0
for fname in legacy_files:
    fpath = repo_dir / fname
    if fpath.exists():
        try:
            shutil.move(str(fpath), str(archive_dir / fname))
            moved_count += 1
        except Exception as e:
            pass

print(f" ✅ Cleaned up {moved_count} legacy files into scratch/archive_legacy_scripts/")
