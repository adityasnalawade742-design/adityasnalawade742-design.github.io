---
name: storefront-catalog-admin
description: >-
  Admin procedures for managing index.html storefront catalog, updating JSON-LD structured schemas,
  category chips (✨ All Finds, 💡 Aesthetic Lighting, 🌿 Room Decor, 🏺 Ceramic Vases, 🪞 Vanity Mirrors),
  45-currency switcher exchange rates, and executing single-click product deletions via delete_product.py.
  Use when adding/removing catalog items, updating currency dropdowns, or modifying homepage layout.
---

# 🛍️ Storefront Catalog Administration Skill

This skill defines administrative procedures for maintaining the luxury storefront page ([`index.html`](file:///G:/CLI/pinterest-auto-affiliate/index.html)), managing catalog entries in `product_price_registry.json`, and configuring multi-currency exchange rate engines.

---

## ⚙️ Core Administration Tasks

### 1. Single-Click Product Deletion (`delete_product.py`)
Completely purge an ASIN campaign from the entire platform:
```bash
python delete_product.py B0D8P8CSYP
```
**Purge Operations Executed**:
- Removes product card (`#card-{asin}`) from `index.html`.
- Deletes `bridge_{asin}.html` from root and `bridge_pages/`.
- Deletes image assets (`focus_product_{asin}_hook.jpg`, `raw_images/raw_{asin}.jpg`).
- Removes entry from `product_price_registry.json` and `processed_asins.json`.
- Updates JSON-LD schema on `index.html`.
- Auto-commits and pushes deletions to GitHub Pages.

---

### 2. Homepage Category Chips & Filtering Rules
`index.html` features instant client-side filtering via category chips:
- `✨ All Finds` (`data-category="all"`)
- `💡 Aesthetic Lighting` (`data-category="lighting"`)
- `🌿 Room Decor` (`data-category="decor"`)
- `🏺 Ceramic Vases` (`data-category="vases"`)
- `🪞 Vanity Mirrors` (`data-category="mirrors"`)

**Rule**: Every card on `index.html` MUST have a clean, lower-case singular `data-category` attribute matching one of the 4 primary catalog categories (`lighting`, `decor`, `vases`, `mirrors`).

Check category alignment:
```bash
python scratch/check_homepage_categories.py
```

---

### 3. Google JSON-LD Structured Data Schema (`index.html`)
The `<head>` of `index.html` contains schema.org `ItemList` JSON-LD data for Googlebot SEO ranking:
```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "numberOfItems": 9,
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Flame Aroma Essential Oil Diffuser",
      "url": "https://adityasnalawade742-design.github.io/bridge_B0GYDXHF4G.html"
    }
  ]
}
```
Re-sync JSON-LD schema with active registry items:
```bash
python sync_direct_matrix_and_registry.py
```

---

### 4. 45-Currency Real-Time Exchange Rate Engine
`index.html` and all bridge pages fetch live currency exchange rates from Open Exchange Rates API:
- Endpoint: `https://open.er-api.com/v6/latest/USD`
- Native Banking Formatters:
  - 🇺🇸 US / 🇮🇳 IN / 🇬🇧 UK / 🇨🇦 CA / 🇦🇺 AU: Period decimal (`$32.99`, `₹2,754.67`).
  - 🇪🇺 Europe: Comma decimal with space (`18,40 €`).
  - 🇯🇵 Japan: Pure integer formatting (`¥3,100`).

---

## 📋 Catalog Administration Checklist
- [ ] Card count on `index.html` matches number of active entries in `product_price_registry.json`.
- [ ] Search input clear button (`✕`) resets filter and restores all gallery cards.
- [ ] Admin mode (`index.html?admin=true`) reveals delete buttons; public mode conceals them.
- [ ] `sitemap.xml` contains all active bridge landing page URLs.
