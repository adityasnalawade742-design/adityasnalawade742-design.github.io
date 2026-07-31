import sys
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")
total_untagged = 0
for lp in repo.glob("bridge_*.html"):
    text = lp.read_text(encoding="utf-8")
    links = re.findall(r'href="(https://www\.amazon\.[^"]+)"', text)
    untagged = [l for l in links if "tag=" not in l]
    if untagged:
        total_untagged += len(untagged)
        print(f"📄 {lp.name}: Found {len(untagged)} untagged links:")
        for u in untagged:
            print(f"   - {u}")

print(f"\nTotal untagged links across all landing pages: {total_untagged}")
