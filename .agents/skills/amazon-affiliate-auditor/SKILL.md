---
name: amazon-affiliate-auditor
description: >-
  Specialized auditor skill for Amazon Associate link integrity, 21-domain regional Store IDs,
  product data scraping, price handling, FTC disclosure compliance, and zero-404 geo-redirection.
  Use when auditing Amazon affiliate links, checking ASIN data accuracy, or verifying tag compliance.
---

# 🛒 Amazon Affiliate Auditor Skill (`amazon-affiliate-auditor`)

This skill defines the audit procedure for inspecting Amazon Associate links, ASIN data integrity, regional Store IDs, pricing accuracy, and FTC disclosure compliance.

---

## 🛠️ Audit Checklist & Diagnostic Commands

### 1. Associate Tag Verification
Ensure official Store IDs are mapped correctly across 21 domains in `affiliate_tag_config.json`:
- `amazon.com`: `smartdeal0358-20`
- `amazon.in`: `smartdeal0358-21`
- `amazon.co.uk`: `smartdea04b3a-21`
- `amazon.de`: `smartdeal0bb4-21`
- `amazon.fr`: `smartdeal0962-21`
- `amazon.es`: `smartdeal0b46-21`
- `amazon.it`: `smartdea03a8d-21`

Run URL validator script:
```bash
python validate_all_affiliate_urls.py
python audit_all_affiliate_tags.py
```

### 2. Product Data & Price Synchronization Audit
- Extract live product details:
  ```python
  from modules.amazon_extractor import get_product_details_and_photos
  print(get_product_details_and_photos("B0BZXNSW5K"))
  ```
- Compare live Amazon price against `product_price_registry.json`, `index.html`, and `bridge_*.html`.
- Run health check:
  ```bash
  python run_daily_health_check.py
  ```

### 3. 21-Domain Geo-Matrix & 0ms Redirection Audit
- Verify matrix mappings in `global_direct_matrix.json`.
- Execute 189-point Playwright zero-404 audit script:
  ```bash
  python scratch/master_zero_404_audit.py
  ```

### 4. FTC Disclosure & Compliance Audit
Ensure every bridge landing page (`bridge_*.html`) contains prominent FTC affiliate disclosures:
- Banner text: *"As an Amazon Associate I earn from qualifying purchases."*
- Outbound CTA buttons explicitly styled with Amazon brand logos and country flags (*e.g., "VIEW DEAL ON AMAZON US ($)"*).
