---
name: zero-404-geo-matrix-manager
description: >-
  Standard operating procedure for verifying live Amazon listings across 21 international domains,
  updating global_direct_matrix.json, auditing affiliate tags (smartdeal0358-21), and running
  the 189-point Playwright zero-404 audit script. Use when testing international availability,
  validating geo-redirection scripts, or onboarding new regional Amazon store IDs.
---

# 🌐 Zero-404 Geo-Matrix & Affiliate Link Manager Skill

This skill defines the rules, data structures, and verification workflows for managing the **Universal Multi-Region Geo-Redirector Engine** (`modules/bridge_creator.py`) across 21 international Amazon domains.

---

## 🏛️ System Principles & Zero-404 Guarantee

1. **0ms Instant Synchronous Redirection**:
   Detects visitor location synchronously using browser timezone (`Asia/Kolkata`, `Europe/London`, `Asia/Tokyo`) and language signals (`en-IN`, `hi`). Operates before external IP lookups fire.

2. **Empirical Direct Matrix Rules (`global_direct_matrix.json`)**:
   - **Direct ASIN Page (`/dp/{asin}`)**: Listed ONLY when HTTP 200 live listing existence has been empirically verified via Playwright / Requests.
   - **Targeted Category Search Fallback (`/s?k={keywords}`)**: Triggered when the exact ASIN code is not directly listed in that specific country. Buyers land on live relevant local product search results.
   - **Zero 404 Guarantee**: Eliminates Amazon's internal *"Looking for something? We're sorry"* 404 page across 100% of global visits.

3. **100% Revenue Protection Tag Rule**:
   - Primary Store ID: `smartdeal0358-21` (India, US default)
   - Regional Store IDs (`affiliate_tag_config.json`):
     - 🇺🇸 US / 🇲🇽 MX / 🇧🇷 BR / 🇸🇬 SG / 🇦🇪 AE / 🇸🇦 SA / 🇪🇬 EG / 🇯🇵 JP / 🇦🇺 AU: `smartdeal0358-20`
     - 🇮🇳 India: `smartdeal0358-21`
     - 🇬🇧 UK: `smartdea04b3a-21`
     - 🇩🇪 DE / 🇸🇪 SE / 🇳🇱 NL / 🇵🇱 PL / 🇹🇷 TR: `smartdeal0bb4-21`
     - 🇫🇷 FR / 🇧🇪 BE: `smartdeal0962-21`
     - 🇪🇸 ES: `smartdeal0b46-21`
     - 🇮🇹 IT: `smartdea03a8d-21`

---

## 🛠️ Diagnostics & Audit Commands

### Command 1: Run 189-Point Zero 404 Audit Script
Executes Playwright headless tests for all catalog ASINs across all 21 Amazon domains:
```bash
python scratch/master_zero_404_audit.py
```

---

### Command 2: Validate All Outbound Affiliate URLs
Crawls all local bridge landing pages and checks URL parameters for official Store IDs and encodings:
```bash
python validate_all_affiliate_urls.py
```

---

### Command 3: Audit Affiliate Tags on Index Storefront
Ensures tag `smartdeal0358-21` is attached to 100% of card CTA links on `index.html`:
```bash
python audit_all_affiliate_tags.py
```

---

### Command 4: Test Live Amazon Page Existence
Pings live Amazon storefronts to build or update `global_direct_matrix.json`:
```bash
python scratch/test_live_amazon_404.py
```

---

### Command 5: Sync Direct Matrix & Registry
Synchronizes matrix changes with registry and JSON-LD schema on `index.html`:
```bash
python sync_direct_matrix_and_registry.py
```

---

## 🔒 Security & Revenue Rules
1. **Never manual-add without verification**: NEVER add a country code to `global_direct_matrix.json` without verifying live HTTP 200 listing existence.
2. **Affiliate Tag Guard**: `smartdeal0358-21` (or official regional Store ID) MUST remain attached to 100% of outgoing CTA links.
3. **No Breaking Lints or 404s**: Rebuild and test all landing pages before pushing live using `rebuild_EVERY_single_bridge.py`.
