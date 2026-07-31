import sys
import os
from pathlib import Path
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")

raw1 = repo / "raw_images" / "raw_B0D8P8CSYP.jpg"
raw2 = repo / "raw_B0D8P8CSYP_console.jpg"

print("==================================================")
print("🕒 FILE MODIFICATION TIMESTAMPS FOR BIRD LAMP")
print("==================================================")

if raw1.exists():
    mtime1 = datetime.fromtimestamp(os.path.getmtime(raw1)).strftime('%Y-%m-%d %H:%M:%S')
    print(f" • raw_images/raw_B0D8P8CSYP.jpg: {mtime1} (Size: {raw1.stat().st_size} bytes)")
else:
    print(" • raw_images/raw_B0D8P8CSYP.jpg: Not found")

if raw2.exists():
    mtime2 = datetime.fromtimestamp(os.path.getmtime(raw2)).strftime('%Y-%m-%d %H:%M:%S')
    print(f" • raw_B0D8P8CSYP_console.jpg:     {mtime2} (Size: {raw2.stat().st_size} bytes)")
else:
    print(" • raw_B0D8P8CSYP_console.jpg: Not found")
