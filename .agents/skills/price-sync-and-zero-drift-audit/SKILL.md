---
name: price-sync-and-zero-drift-audit
description: >-
  Operational runbook for synchronizing global Amazon prices daily, executing zero-drift self-healing checks,
  re-rendering graphic price badges from clean raw images, updating index.html data attributes,
  and deploying cache-busted updates to GitHub Pages. Use when checking price drift, running health checks,
  or troubleshooting daily scheduled sync jobs.
---

# 🔄 Price Synchronization & Zero-Drift Audit Skill

This skill defines the routine execution procedures for maintaining 100% price alignment across `product_price_registry.json`, `index.html`, Jinja2 landing pages (`bridge_*.html`), and Playwright graphic overlays (`focus_product_{asin}_hook.jpg`).

---

## 🛠️ CLI Runbook & Command Sequence

### Command 1: Run Daily Automated Price Synchronizer
Scrapes live Amazon listing prices for all active ASINs and re-renders Playwright badges:
```bash
python daily_price_updater.py
```
- Compares live scraped prices against `product_price_registry.json`.
- If a price change is detected ($old \neq new$):
  1. Re-renders the Playwright graphic overlay onto clean text-free image `raw_images/raw_{asin}.jpg`.
  2. Updates `<div class="price">` inside `bridge_{asin}.html`.
  3. Updates `<div class="card-price-tag">` and `data-price-usd` inside `index.html`.
  4. Saves updated registry values to `product_price_registry.json`.

---

### Command 2: Execute Master Multi-Region Price Sync
Synchronizes price data across all 21 international Amazon domains and scrapes local currencies:
```bash
python sync_all_regional_prices_master.py
```
Or use the lightweight task scheduler entrypoint:
```bash
python sync_exact_amazon_prices.py
```

---

### Command 3: Execute Zero-Drift Self-Healing Bot
Checks 100% of price values across all catalog files to detect and heal 1-penny/rupee discrepancies:
```bash
python run_daily_health_check.py
```
**Self-Healing Actions Performed**:
- Cleans INR/currency symbol contamination in USD fields.
- Corrects `data-price-usd` attributes on `index.html` gallery cards.
- Purges orphaned temporary raw images.
- Auto-commits and pushes healed files to GitHub Pages.

---

### Command 4: Verify Index Storefront Alignment
Run static diagnostic checks on `index.html` pricing and attributes:
```bash
python scratch/audit_index_prices.py
```
Or force complete clean synchronization from registry:
```bash
python scratch/sync_index_html_clean.py
```

---

## 🔒 Cache-Busting Deployment Guidelines
When deploying updated images or landing pages to GitHub Pages, always enforce cache-busting to bypass browser caching:
1. Append version/timestamp query parameters to image URIs: `focus_product_{asin}_hook.jpg?v={timestamp}`.
2. Use dynamic filename suffixes when generating new graphics: `focus_product_{asin}_exact2vases_hook.jpg`.
3. Auto-deploy to GitHub Pages using master rebuilder:
   ```bash
   python rebuild_EVERY_single_bridge.py
   ```

---

## 📋 Verification Checklist
- [ ] Registered price in `product_price_registry.json` equals live Amazon listing price.
- [ ] Card price tag in `index.html` (`#card-{asin} .card-price-tag`) matches registered price.
- [ ] Hero price in `bridge_{asin}.html` (`.price`) matches registered price.
- [ ] Graphic image `focus_product_{asin}_hook.jpg` displays updated price tag.
- [ ] Working tree clean and pushed to GitHub main branch (`git status`).
