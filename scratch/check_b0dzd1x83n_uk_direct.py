import sys
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

url = "https://www.amazon.co.uk/dp/B0DZD1X83N"
r = requests.get(url, headers=headers, timeout=8)
print(f"Amazon UK HTTP Status for B0DZD1X83N: {r.status_code}")
print("Contains product title:", "Wood" in r.text or "Lamp" in r.text)
