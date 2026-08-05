import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path('.').resolve()
reg_file = repo / 'product_price_registry.json'
registry = json.loads(reg_file.read_text(encoding='utf-8'))

print('Current registry price for B07HP22QTZ:', registry.get('B07HP22QTZ', {}).get('current_price'))

# 1. Update registry
registry['B07HP22QTZ']['current_price'] = '$9.99'
registry['B07HP22QTZ']['regional_prices']['US'] = '$9.99'
reg_file.write_text(json.dumps(registry, indent=2), encoding='utf-8')
print('Updated product_price_registry.json for B07HP22QTZ to $9.99')

# 2. Rebuild price badges
sys.path.append(str(repo))
from rebuild_all_price_badges_usd import rebuild_all_price_badges
rebuild_all_price_badges()

# 3. Update index.html
idx_file = repo / 'index.html'
idx_content = idx_file.read_text(encoding='utf-8')

# Update data-price-us and card-price-tag for card-B07HP22QTZ
card_block_pattern = r'(id="card-B07HP22QTZ"[^>]*>[\s\S]*?<div class="card-price-tag">)[^<]+(</div>)'
idx_content = re.sub(card_block_pattern, r'\g<1>$9.99\g<2>', idx_content)

idx_file.write_text(idx_content, encoding='utf-8')
print('Updated index.html card price tag for B07HP22QTZ to $9.99')
