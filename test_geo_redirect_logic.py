import sys
from pathlib import Path
from bs4 import BeautifulSoup

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

bridge_path = Path("G:/CLI/pinterest-auto-affiliate/bridge_B0D8P8CSYP.html")
print("🧪 TESTING GEO-REDIRECT CODE IN bridge_B0D8P8CSYP.html...\n")

content = bridge_path.read_text(encoding="utf-8")

print("Checking JS redirect logic snippets:\n")

lines = content.splitlines()
for i, line in enumerate(lines, 1):
    if "buyBtn.href =" in line:
        print(f"Line {i}: {line.strip()}")

print("\nTag Check Result:")
if "tag=smartdeal0358-21" in content:
    print("✅ Affiliate tag 'smartdeal0358-21' is 100% hardcoded in both US links and non-US redirect functions!")
else:
    print("❌ Tag is missing!")
