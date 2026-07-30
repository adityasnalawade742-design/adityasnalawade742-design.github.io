import sys
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

urls = [
    "https://adityasnalawade742-design.github.io/bridge_B0DZD1X83N.html",
    "https://adityasnalawade742-design.github.io/bridge_B0GYDXHF4G.html",
    "https://adityasnalawade742-design.github.io/bridge_B0FXLYXM32.html",
    "https://adityasnalawade742-design.github.io/bridge_B0C2YLN3H4.html",
    "https://adityasnalawade742-design.github.io/bridge_B07HP22QTZ.html",
    "https://adityasnalawade742-design.github.io/bridge_B0BZXNSW5K.html",
    "https://adityasnalawade742-design.github.io/bridge_B0DXKGL1T2.html",
    "https://adityasnalawade742-design.github.io/bridge_B0D1FRDFFX.html",
    "https://adityasnalawade742-design.github.io/bridge_B0D8P8CSYP.html"
]

print("==================================================")
print("🌐 CHECKING LIVE GITHUB PAGES URL STATUS")
print("==================================================")

for u in urls:
    try:
        r = requests.get(u, timeout=8)
        print(f" • {u.split('/')[-1]:22s} -> Status: {r.status_code}")
    except Exception as e:
        print(f" • {u.split('/')[-1]:22s} -> Error: {e}")
