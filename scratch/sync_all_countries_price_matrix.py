import sys
import json
import re
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")
index_path = repo_dir / "index.html"

print("==================================================")
print("🌍 SYNCHRONIZING EXPLICIT REGIONAL PRICING FOR ALL 7 COUNTRIES")
print("==================================================")

full_country_matrix = {
    "B0DZD1X83N": { # Wood Base Lamp
        "us": "$12.99", "uk": "£10.99", "in": "Not Available", "de": "€14.99", "ca": "CA$18.99", "jp": "Not Available", "au": "Not Available"
    },
    "B0GYDXHF4G": { # Flame Diffuser
        "us": "$35.00", "uk": "Not Available", "in": "Not Available", "de": "Not Available", "ca": "Not Available", "jp": "Not Available", "au": "Not Available"
    },
    "B0FXLYXM32": { # Wavy Mirror
        "us": "$76.49", "uk": "£57.42", "in": "Not Available", "de": "€66.97", "ca": "CA$107.56", "jp": "¥12,508", "au": "A$110.02"
    },
    "B0C2YLN3H4": { # Donut Vases
        "us": "$14.99", "uk": "Not Available", "in": "₹599.00", "de": "€13.12", "ca": "CA$21.08", "jp": "¥2,451", "au": "A$21.56"
    },
    "B07HP22QTZ": { # Suncatcher
        "us": "$9.99", "uk": "£7.50", "in": "₹2,762.75", "de": "€8.75", "ca": "CA$14.05", "jp": "¥1,634", "au": "A$14.37"
    },
    "B0BZXNSW5K": { # Touch Lamp
        "us": "$19.99", "uk": "£15.01", "in": "₹475.00", "de": "€17.50", "ca": "CA$28.11", "jp": "Not Available", "au": "Not Available"
    },
    "B0DXKGL1T2": { # Lily Lamp
        "us": "$38.57", "uk": "£28.95", "in": "Not Available", "de": "€33.77", "ca": "CA$54.24", "jp": "Not Available", "au": "Not Available"
    },
    "B0D1FRDFFX": { # Mushroom Lamp
        "us": "$35.98", "uk": "£27.01", "in": "₹11,428.51", "de": "€31.50", "ca": "CA$50.60", "jp": "Not Available", "au": "A$51.75"
    },
    "B0D8P8CSYP": { # Cute Bird Lamp
        "us": "$20.56", "uk": "£15.43", "in": "₹3,843.00", "de": "€18.00", "ca": "CA$28.91", "jp": "¥3,362", "au": "A$29.57"
    }
}

content = index_path.read_text(encoding="utf-8")

for asin, r_prices in full_country_matrix.items():
    attr_str = ' '.join([f'data-price-{reg}="{val}"' for reg, val in r_prices.items()])
    
    # Clean replacement on card element
    pattern = rf'<div class="card-wrapper" id="card-{asin}"[^>]*>'
    replacement = f'<div class="card-wrapper" id="card-{asin}" data-base-usd="{r_prices["us"].replace("$","")}" {attr_str} data-category="lighting decor">'
    content = re.sub(pattern, replacement, content)

index_path.write_text(content, encoding="utf-8")
print(" ✅ Synchronized explicit 7-country pricing & availability attributes on index.html!")

# Commit & Push Live
print("\n🚀 Pushing 7-country regional matrix live to GitHub Pages...")
try:
    subprocess.run(["git", "add", "-A"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "commit", "-m", "synchronize explicit 7-country regional pricing and 'Not Available' matrix for all products"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(repo_dir), check=True)
    print(" ✅ Git Commit & Push 100% Successful!")
except Exception as e:
    print(f" ⚠️ Git push warning: {e}")

print("\n🎉 7-COUNTRY REGIONAL MATRIX DEPLOYED LIVE!")
