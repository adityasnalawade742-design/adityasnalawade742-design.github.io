import sys
import io
import os
import re
import subprocess
from pathlib import Path

# UTF-8 encoding fix for Windows PowerShell
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def delete_product(product_id: str):
    """
    Deletes a product campaign from the project:
    1. Removes root & output bridge page HTML
    2. Removes root & output focus product images
    3. Removes card from root index.html
    4. Pushes changes to GitHub main & gh-pages
    """
    product_id = product_id.strip()
    if not product_id:
        print("❌ Error: Please provide a Product ID or ASIN (e.g. python delete_product.py B0D1FRDFFX)")
        sys.exit(1)

    project_root = Path(__file__).resolve().parent
    output_dir = project_root / "output"

    print(f"🗑️ Deleting campaign files for Product ID: {product_id}...")

    # Files to remove
    files_to_remove = [
        project_root / f"bridge_{product_id}.html",
        project_root / f"focus_product_{product_id}_hook.jpg",
        project_root / f"focus_product_{product_id}.jpg",
        output_dir / "bridge_pages" / f"bridge_{product_id}.html",
        output_dir / "images" / f"focus_product_{product_id}_hook.jpg",
        output_dir / "images" / f"focus_product_{product_id}.jpg",
        output_dir / "images" / f"product_{product_id}_ref_sheet.jpg"
    ]

    removed_count = 0
    for file_path in files_to_remove:
        if file_path.exists():
            file_path.unlink()
            print(f"  ✓ Deleted file: {file_path.name}")
            removed_count += 1

    # Remove card from index.html
    index_file = project_root / "index.html"
    if index_file.exists():
        with open(index_file, "r", encoding="utf-8") as f:
            html = f.read()

        card_pattern = rf'(<!--\s*Card\s+{product_id}\s*-->\s*)?<div\s+class="card-wrapper"\s+id="card-{product_id}">[\s\S]*?</div>\s*</div>\s*'
        updated_html = re.sub(card_pattern, '', html, flags=re.IGNORECASE)


        if updated_html != html:
            with open(index_file, "w", encoding="utf-8") as f:
                f.write(updated_html)
            print(f"  ✓ Removed product card from index.html!")

    # Remove from product_price_registry.json
    registry_file = project_root / "product_price_registry.json"
    if registry_file.exists():
        try:
            with open(registry_file, "r", encoding="utf-8") as f:
                reg = json.load(f)
            if product_id in reg:
                del reg[product_id]
                with open(registry_file, "w", encoding="utf-8") as f:
                    json.dump(reg, f, indent=2)
                print(f"  ✓ Removed {product_id} from product_price_registry.json!")
        except Exception as e:
            print(f"  ⚠️ Registry update error: {e}")

    # Remove from processed_asins.json
    processed_file = project_root / "processed_asins.json"
    if processed_file.exists():
        try:
            with open(processed_file, "r", encoding="utf-8") as f:
                proc = json.load(f)
            if product_id in proc:
                proc.remove(product_id)
                with open(processed_file, "w", encoding="utf-8") as f:
                    json.dump(proc, f, indent=2)
                print(f"  ✓ Removed {product_id} from processed_asins.json!")
        except Exception as e:
            print(f"  ⚠️ Processed history update error: {e}")

    print("\n🚀 Pushing deletion update to GitHub Pages...")
    try:
        subprocess.run(["git", "add", "-A"], check=True, cwd=str(project_root))
        subprocess.run(["git", "commit", "-m", f"Delete product campaign {product_id}"], check=False, cwd=str(project_root))
        subprocess.run(["git", "push", "origin", "main"], check=True, cwd=str(project_root))
        print(f"\n🎉 SUCCESS: Product {product_id} completely deleted and synced live on GitHub Pages!")
    except Exception as e:
        print(f"⚠️ Git push warning: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python delete_product.py <ASIN_OR_PRODUCT_ID>")
        sys.exit(1)
    delete_product(sys.argv[1])
