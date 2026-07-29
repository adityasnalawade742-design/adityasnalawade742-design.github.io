import sys
import time
import re
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

asin = "B0BZXNSW5K"
ts = int(time.time())
cache_buster = f"v=user_photo_{ts}"

bridge_file = Path(f"G:/CLI/pinterest-auto-affiliate/bridge_{asin}.html")
content = bridge_file.read_text(encoding="utf-8")
content = re.sub(r'focus_product_B0BZXNSW5K_hook\.jpg(?:\?v=[^\'"]+)?', f'focus_product_B0BZXNSW5K_hook.jpg?{cache_buster}', content)
bridge_file.write_text(content, encoding="utf-8")
print(f"✅ Updated bridge_{asin}.html with cache buster ?{cache_buster}")

index_file = Path("G:/CLI/pinterest-auto-affiliate/index.html")
content = index_file.read_text(encoding="utf-8")
content = re.sub(r'focus_product_B0BZXNSW5K_hook\.jpg(?:\?v=[^\'"]+)?', f'focus_product_B0BZXNSW5K_hook.jpg?{cache_buster}', content)
index_file.write_text(content, encoding="utf-8")
print(f"✅ Updated index.html with cache buster ?{cache_buster}")

subprocess.run(["git", "add", "-A"], check=True)
subprocess.run(["git", "commit", "-m", f"apply user generated image b9e65w6bf9rn80cznt1tap5v28 onto focus_product_B0BZXNSW5K_hook.jpg ({cache_buster})"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)
print("🚀 Git Commit & Push Successful!")
