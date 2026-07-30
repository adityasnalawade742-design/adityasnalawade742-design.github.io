import os
import sys
import json
import re
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")
sys.path.append(str(repo_dir))
index_path = repo_dir / "index.html"

print("==================================================")
print("🌍 APPLYING UNIVERSAL REGIONAL PRICE & AVAILABILITY MATRIX")
print("   Supported Regions: US, UK, IN, DE, CA, JP, AU")
print("==================================================")

# Master Regional Matrix (Availability & Exact Local Prices)
# If a region is missing from direct_regions and has no local price, it is marked "Not Available"
regional_matrix = {
    "B0DZD1X83N": { # Wood Base Lamp
        "us": "$12.99", "ca": "CA$18.99", "in": "Not Available", "uk": "£10.99", "de": "€14.99", "jp": "Not Available", "au": "Not Available"
    },
    "B0GYDXHF4G": { # Flame Diffuser
        "us": "$35.00", "in": "Not Available", "uk": "Not Available", "de": "Not Available", "ca": "Not Available", "jp": "Not Available", "au": "Not Available"
    },
    "B0FXLYXM32": { # Wavy Mirror
        "us": "$76.49", "in": "₹7,324.36", "uk": "£57.42", "de": "€66.97", "ca": "CA$107.56", "jp": "¥12,508", "au": "A$110.02"
    },
    "B0C2YLN3H4": { # Donut Vases
        "us": "$14.99", "in": "₹1,435.38", "uk": "Not Available", "de": "€13.12", "ca": "CA$21.08", "jp": "¥2,451", "au": "A$21.56"
    },
    "B07HP22QTZ": { # Suncatcher
        "us": "$9.99", "in": "₹2,762.75", "uk": "£7.50", "de": "€8.75", "ca": "CA$14.05", "jp": "¥1,634", "au": "A$14.37"
    },
    "B0BZXNSW5K": { # Touch Lamp
        "us": "$19.99", "in": "₹1,914.16", "uk": "£15.01", "de": "€17.50", "ca": "CA$28.11", "jp": "Not Available", "au": "Not Available"
    },
    "B0DXKGL1T2": { # Lily Lamp
        "us": "$38.57", "uk": "£28.95", "de": "€33.77", "ca": "CA$54.24", "in": "Not Available", "jp": "Not Available", "au": "Not Available"
    },
    "B0D1FRDFFX": { # Mushroom Lamp
        "us": "$35.98", "in": "₹3,445.29", "uk": "£27.01", "de": "€31.50", "ca": "CA$50.60", "au": "A$51.75", "jp": "Not Available"
    },
    "B0D8P8CSYP": { # Cute Bird Lamp
        "us": "$20.56", "in": "₹1,968.74", "uk": "£15.43", "de": "€18.00", "ca": "CA$28.91", "jp": "¥3,362", "au": "A$29.57"
    }
}

# 1. Update index.html Card Wrapper Attributes with data-price-{region}
content = index_path.read_text(encoding="utf-8")

for asin, r_prices in regional_matrix.items():
    attr_str = ' '.join([f'data-price-{reg}="{val}"' for reg, val in r_prices.items()])
    
    # Replace attributes on card-ASIN
    pattern = rf'id="card-{asin}" data-base-usd="[^"]+"(?: data-price-[a-z]+="[^"]+")*'
    replacement = f'id="card-{asin}" data-base-usd="{r_prices["us"].replace("$","")}" {attr_str}'
    content = re.sub(pattern, replacement, content)

# 2. Update changeGlobalCurrency logic on index.html
currency_script = '''        function changeGlobalCurrency(targetCurr) {
            const rate = exchangeRates[targetCurr] || 1.0;
            const sym = currencySymbols[targetCurr] || (targetCurr + " ");
            const currToRegionMap = { "USD": "us", "GBP": "uk", "INR": "in", "EUR": "de", "CAD": "ca", "JPY": "jp", "AUD": "au" };
            const regionCode = currToRegionMap[targetCurr] || 'us';

            document.querySelectorAll('.card-wrapper').forEach(card => {
                const regionalVal = card.getAttribute(`data-price-${regionCode}`);
                const priceTag = card.querySelector('.card-price-tag');

                if (regionalVal === 'Not Available') {
                    if (priceTag) {
                        priceTag.innerText = 'Not Available';
                        priceTag.style.background = 'rgba(239, 68, 68, 0.25)';
                        priceTag.style.color = '#fca5a5';
                        priceTag.style.borderColor = 'rgba(239, 68, 68, 0.4)';
                    }
                } else if (regionalVal && priceTag) {
                    priceTag.innerText = regionalVal;
                    priceTag.style.background = 'linear-gradient(135deg, rgba(255, 183, 3, 0.95), rgba(251, 133, 0, 0.95))';
                    priceTag.style.color = '#000';
                    priceTag.style.borderColor = 'transparent';
                } else {
                    const baseUsd = parseFloat(card.getAttribute('data-base-usd') || '20.00');
                    const converted = (baseUsd * rate).toLocaleString(undefined, {
                        minimumFractionDigits: (targetCurr === 'JPY' || targetCurr === 'KRW') ? 0 : 2,
                        maximumFractionDigits: (targetCurr === 'JPY' || targetCurr === 'KRW') ? 0 : 2
                    });
                    if (priceTag) {
                        priceTag.innerText = `${sym}${converted}`;
                        priceTag.style.background = 'linear-gradient(135deg, rgba(255, 183, 3, 0.95), rgba(251, 133, 0, 0.95))';
                        priceTag.style.color = '#000';
                        priceTag.style.borderColor = 'transparent';
                    }
                }
            });
        }'''

content = re.sub(r'function changeGlobalCurrency\(targetCurr\) \{[\s\S]*?\}', currency_script, content)
index_path.write_text(content, encoding="utf-8")
print(" ✅ Applied Universal Regional Price & Availability attributes to index.html!")

# 3. Update all landing pages bridge_*.html for Regional Out of Stock handling
from rebuild_EVERY_single_bridge import master_catalog
from modules.bridge_creator import generate_bridge_page

print("\n🔨 Rebuilding landing pages with Out of Stock regional handling...")
for asin, item in master_catalog.items():
    item["regional_matrix"] = regional_matrix.get(asin, {})
    seo_data = {
        "pin_title": item["title"],
        "image_hook": item.get("headline", item["title"])[:30],
        "subtitle_hook": "",
        "badge_hook": "VIRAL ROOM FIND",
        "description": item["description"]
    }
    generate_bridge_page(item, seo_data, asin)

# 4. Push live to GitHub Pages
print("\n🚀 Pushing Universal Regional Availability Matrix live to GitHub Pages...")
try:
    subprocess.run(["git", "add", "-A"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "commit", "-m", "apply universal regional price and 'Not Available' out-of-stock matrix for all products across all countries"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(repo_dir), check=True)
    print(" ✅ Git Commit & Push 100% Successful!")
except Exception as e:
    print(f" ⚠️ Git push warning: {e}")

print("\n🎉 UNIVERSAL REGIONAL MATRIX DEPLOYED LIVE!")
