"""
Interactive Image Verification & Selection Module
Extracts, scores, and presents Amazon listing photos for user confirmation/selection.
"""
import sys
import io

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from modules.amazon_extractor import (
    has_text_annotation,
    is_grid_collage,
    has_human_presence,
    calculate_cozy_vibe_score,
    select_clean_photo_or_skip
)

def verify_and_select_product_photo(photos: list, product_title: str = "", default_auto: bool = False) -> tuple[str, list]:
    """
    Analyzes all Amazon listing photos, prints a structured photo audit table with clickable URLs,
    and returns (selected_photo_url, all_scored_photos).
    """
    if not photos:
        return ("", [])

    print("\n" + "="*70)
    print("📸 INTERACTIVE IMAGE VERIFICATION & QUALITY AUDIT")
    print(f"Product: {product_title[:60]}...")
    print("="*70)

    analyzed = []
    for idx, url in enumerate(photos, 1):
        if not url or not url.startswith("http"):
            continue
        
        has_txt = has_text_annotation(url)
        has_grid = is_grid_collage(url)
        has_human = has_human_presence(url)
        
        is_clean = (not has_txt) and (not has_grid) and (not has_human)
        score = calculate_cozy_vibe_score(url) if is_clean else 0.0

        status_flags = []
        if has_txt:
            status_flags.append("Text Overlay")
        if has_grid:
            status_flags.append("Split Collage")
        if has_human:
            status_flags.append("Human/Hand")

        status_str = f"DISCARDED ({', '.join(status_flags)})" if status_flags else f"CLEAN (Score: {score:.1f}/10)"

        analyzed.append({
            "index": idx,
            "url": url,
            "is_clean": is_clean,
            "score": score,
            "status": status_str
        })

    # Display photo analysis table
    print("\n[Extracted Listing Photos Audit]")
    for item in analyzed:
        badge = "🏆 RECOMMENDED" if item["score"] > 0 and item["score"] == max((x["score"] for x in analyzed if x["is_clean"]), default=-1) else ""
        print(f"  Photo [{item['index']}]: {item['status']} {badge}")
        print(f"    URL: {item['url']}")

    # Select auto winner
    clean_items = [x for x in analyzed if x["is_clean"]]
    if clean_items:
        clean_items.sort(key=lambda x: x["score"], reverse=True)
        recommended = clean_items[0]["url"]
        rec_index = clean_items[0]["index"]
    else:
        recommended = photos[0] if photos else ""
        rec_index = 1

    print("\n" + "-"*70)
    print(f"⭐️ #1 AI Recommended Photo: Photo [{rec_index}]")
    print(f"👉 URL: {recommended}")
    print("-"*70)

    return (recommended, analyzed)
