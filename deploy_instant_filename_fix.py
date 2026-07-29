import sys
import shutil
import subprocess
from pathlib import Path

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

asin = "B0BZXNSW5K"
src_user_img = Path("G:/CLI/pinterest-auto-affiliate/b9e65w6bf9rn80cznt1tap5v28.jpg")
new_filename = f"focus_product_{asin}_hook_b9e65.jpg"
dst_img = Path(f"G:/CLI/pinterest-auto-affiliate/{new_filename}")

print(f"📦 Copying user image to new unique filename: {new_filename}...")
shutil.copyfile(src_user_img, dst_img)

# Update bridge page HTML with new filename
bridge_file = Path(f"G:/CLI/pinterest-auto-affiliate/bridge_{asin}.html")
content = bridge_file.read_text(encoding="utf-8")
import re
content = re.sub(rf'focus_product_{asin}_hook[^\'"]*\.jpg(?:\?v=[^\'"]+)?', new_filename, content)
bridge_file.write_text(content, encoding="utf-8")
print(f"✅ Updated bridge_{asin}.html to load {new_filename}")

# Update index.html HTML with new filename
index_file = Path("G:/CLI/pinterest-auto-affiliate/index.html")
content = index_file.read_text(encoding="utf-8")
content = re.sub(rf'focus_product_{asin}_hook[^\'"]*\.jpg(?:\?v=[^\'"]+)?', new_filename, content)
index_file.write_text(content, encoding="utf-8")
print(f"✅ Updated index.html to load {new_filename}")

# Also overwrite default focus_product_B0BZXNSW5K_hook.jpg
shutil.copyfile(src_user_img, Path(f"G:/CLI/pinterest-auto-affiliate/focus_product_{asin}_hook.jpg"))

# Commit & Push Live
subprocess.run(["git", "add", "-A"], check=True)
subprocess.run(["git", "commit", "-m", f"instant cdn update for {asin} with new filename {new_filename}"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)

print("🚀 Successfully pushed new image filename live to GitHub Pages!")
