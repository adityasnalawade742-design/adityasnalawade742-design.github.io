import sys
from pathlib import Path
from bs4 import BeautifulSoup

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")
bridge_files = list(repo.glob("bridge_*.html"))

print(f"Checking raw HTML files for Notice Box visibility (total {len(bridge_files)} files):\n")

for bf in bridge_files:
    content = bf.read_text(encoding="utf-8")
    soup = BeautifulSoup(content, "html.parser")
    box = soup.find(id="geoNoticeBox")
    btn = soup.find(id="buyBtn")
    btn_text = soup.find(id="buyBtnText")
    
    style = box.get("style", "") if box else "NOT FOUND"
    title = soup.find(id="geoNoticeTitle").text.strip() if soup.find(id="geoNoticeTitle") else ""
    href = btn.get("href", "") if btn else ""
    label = btn_text.text.strip() if btn_text else ""
    
    print(f"{bf.name}:")
    print(f"   Notice Box style: \"{style}\"")
    print(f"   Notice Title:     \"{title}\"")
    print(f"   Default href:     \"{href}\"")
    print(f"   Default text:     \"{label}\"\n")
