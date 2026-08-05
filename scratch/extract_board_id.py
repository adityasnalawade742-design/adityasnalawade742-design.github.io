import re
import json
import requests

url = "https://in.pinterest.com/adityasnalawade0703/boho-vases-desk-decor/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5"
}

res = requests.get(url, headers=headers, timeout=10)
print(f"HTTP Status: {res.status_code}")

matches = set()
# Search for numeric board id in HTML JSON payloads
for pattern in [
    r'"board_id":\s*"(\d+)"',
    r'"boardId":\s*"(\d+)"',
    r'"id":\s*"(\d{15,20})"',
    r'board_id=(\d+)',
    r'/boards/(\d+)/'
]:
    found = re.findall(pattern, res.text)
    for f in found:
        matches.add(f)

print(f"Extracted Numeric IDs from {url}:")
for m in matches:
    print(f"  • {m}")
