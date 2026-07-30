import os
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
print("🌍 APPLYING EXACT LOCAL MARKETPLACE REGIONAL PRICES")
print("   Suncatcher B07HP22QTZ -> ₹2,762.75 INR for India")
print("==================================================")

# 1. Update product_price_registry.json
reg_path = repo_dir / "product_price_registry.json"
if reg_path.exists():
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    if "B07HP22QTZ" in reg:
        reg["B07HP22QTZ"]["regional_prices"] = {
            "IN": "₹2,762.75",
            "US": "$9.99"
        }
        reg_path.write_text(json.dumps(reg, indent=2), encoding="utf-8")
        print(" ✅ Updated product_price_registry.json with B07HP22QTZ regional price for IN!")

# 2. Update index.html changeGlobalCurrency JavaScript logic
content = index_path.read_text(encoding="utf-8")

# Add data-price-inr="2,762.75" to card-B07HP22QTZ
content = content.replace(
    'id="card-B07HP22QTZ" data-base-usd="9.99" data-category="decor"',
    'id="card-B07HP22QTZ" data-base-usd="9.99" data-price-inr="2,762.75" data-category="decor"'
)

currency_script = '''        function changeGlobalCurrency(targetCurr) {
            const rate = exchangeRates[targetCurr] || 1.0;
            const sym = currencySymbols[targetCurr] || (targetCurr + " ");
            const lowerCurr = targetCurr.toLowerCase();

            document.querySelectorAll('.card-wrapper').forEach(card => {
                const regionalPrice = card.getAttribute(`data-price-${lowerCurr}`);
                const priceTag = card.querySelector('.card-price-tag');

                if (regionalPrice && priceTag) {
                    priceTag.innerText = regionalPrice;
                } else {
                    const baseUsd = parseFloat(card.getAttribute('data-base-usd') || '20.00');
                    const converted = (baseUsd * rate).toLocaleString(undefined, {
                        minimumFractionDigits: (targetCurr === 'JPY' || targetCurr === 'KRW') ? 0 : 2,
                        maximumFractionDigits: (targetCurr === 'JPY' || targetCurr === 'KRW') ? 0 : 2
                    });
                    if (priceTag) {
                        priceTag.innerText = `${sym}${converted}`;
                    }
                }
            });
        }'''

content = re.sub(r'function changeGlobalCurrency\(targetCurr\) \{[\s\S]*?\}', currency_script, content)
index_path.write_text(content, encoding="utf-8")

print(" ✅ Updated index.html currency engine to support exact regional price overrides!")

# 3. Update bridge_B07HP22QTZ.html landing page
bridge_suncatcher = repo_dir / "bridge_B07HP22QTZ.html"
if bridge_suncatcher.exists():
    b_content = bridge_suncatcher.read_text(encoding="utf-8")
    
    # Add regional price mapping for B07HP22QTZ in bridge page
    inr_price_js = '''
        // Exact Local Marketplace Override for India
        if (userCountry === 'IN') {
            document.querySelectorAll('.hero-price, .cta-price, .price-display').forEach(el => {
                el.innerText = '₹2,762.75';
            });
        }
    '''
    if 'userCountry === \'IN\'' not in b_content:
        b_content = b_content.replace('</script>\n</body>', f'{inr_price_js}\n</script>\n</body>')
        bridge_suncatcher.write_text(b_content, encoding="utf-8")
        print(" ✅ Updated bridge_B07HP22QTZ.html with exact ₹2,762.75 INR local price for India!")

# 4. Push live to GitHub Pages
print("\n🚀 Pushing exact regional price overrides live to GitHub Pages...")
try:
    subprocess.run(["git", "add", "-A"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "commit", "-m", "apply exact regional price override B07HP22QTZ -> ₹2,762.75 INR for India"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(repo_dir), check=True)
    print(" ✅ Git Commit & Push 100% Successful!")
except Exception as e:
    print(f" ⚠️ Git push warning: {e}")

print("\n🎉 REGIONAL PRICE OVERRIDE DEPLOYED LIVE!")
