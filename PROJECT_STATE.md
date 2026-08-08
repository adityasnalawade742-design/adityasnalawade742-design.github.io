# 📌 Pinterest Auto-Affiliate Automation System — Master Project State & Handoff Guide

> **Last Updated**: August 9, 2026  
> **Repository**: `G:\CLI\pinterest-auto-affiliate`  
> **Remote Origin**: `https://github.com/adityasnalawade742-design/adityasnalawade742-design.github.io.git`  
> **Live Showcase**: [https://adityasnalawade742-design.github.io/index.html](https://adityasnalawade742-design.github.io/index.html)  
> **Privacy Policy**: [https://adityasnalawade742-design.github.io/privacy-policy.html](https://adityasnalawade742-design.github.io/privacy-policy.html)  
> **Terms of Service**: [https://adityasnalawade742-design.github.io/terms-of-service.html](https://adityasnalawade742-design.github.io/terms-of-service.html)  
> **Company Name**: Cozy Room Finds  
> **App Name**: Cozy Room Decor Publisher Pro  
> **App ID**: 1596368  
> **Developer Contact Email**: `aditya.s.nalawade742@gmail.com`  
> **Pinterest Account**: `@adityasnalawade0703`  
> **Git Branch**: `main`  
> **System Health Verification Status**: ✅ **100% PASS** (`check_fixes.py` & `test_price_scraper_integrity.py`)  

---

## 1. System Overview

An **end-to-end automated affiliate marketing & landing page generation platform** built for Pinterest traffic. It automatically extracts Amazon product listing data, filters photos for seller text/infographics/hands, applies Playwright high-resolution visual pin overlays with dynamic gradient scrims, builds high-converting glassmorphism landing pages, and routes global visitors across **21 Amazon country storefronts** with zero 404 errors.

---

## 2. Complete Summary of Fixed Issues & New Features

### A. Scraper & Verification Integrity Fixes
- ✅ **Marketplace-Aware Seller Verification (`verify_seller`)**: Replaced unsafe `"amazon" in seller_clean.lower()` with a robust strategy that distinguishes Amazon seller (Case A), third-party seller + Amazon fulfillment (Case B), third-party seller (Case C), and seller unknown (Case D).
- ✅ **Rendered-Page ASIN Identity Verification (`extract_page_asin`)**: Extracts actual ASIN from rendered Amazon pages (`input#ASIN`, `#dp[data-asin]`, `<link rel="canonical">`, and URL redirects) and enforces `detected_asin == target_asin`.
- ✅ **Verified Price Requirement**: Enforced that `STATUS_FRESH_VERIFIED` strictly requires `is_direct == True`, `identity_verified == True`, AND `seller_verified == True`.
- ✅ **Rule 7 Regression Tests**: Added 7 new test cases to `test_price_scraper_integrity.py` (total 16 tests passing).

### B. Read-Only Takeover Audit
- ✅ **12-Point System Audit**: Verified git status, HEAD commit, architecture, scraper architecture, schema, OneLink routing, India routing, geo-detection, test suites, and documentation alignment (Verdict: 🟢 **TAKEOVER CONSISTENT**).

### C. Test Suite & Validation
- ✅ **Full Regression Suite 100% PASS**: `test_price_scraper_integrity.py` (16/16 PASS), `check_fixes.py` (20/20 PASS), `test_affiliate_routing.py` (8/8 PASS), `audit_all_affiliate_tags.py` (23/23 PASS), `validate_all_affiliate_urls.py` (23/23 PASS), `test_bridge_geo_routing.py` (8/8 PASS).

---

## 3. Active Portfolio Products (23 Items)

Catalog consists of 23 active ASINs (`B0FXLYXM32`, `B0C2YLN3H4`, `B07HP22QTZ`, `B0BZXNSW5K`, `B0DXKGL1T2`, `B0D1FRDFFX`, `B0D8P8CSYP`, `B0FGJ1S73D`, `B0CX144DHK`, `B0CJC549C6`, `B0CJ4Q4PZQ`, `B0BQGC76VX`, `B0C7WFZZ7D`, `B0BXP7YWHJ`, `B0D6YRJLCP`, `B0D5YNHXQ7`, `B0BPM41R5C`, `B0DC6HDMRM`, `B0D1G6ZL7Y`, `B0FFG48KCY`, `B0BYP7XB7S`, `B0DQTM3L9J`, `B0CM5RK1K5`).

---

## 4. How to Resume Work in Any Session or AGY Account

When starting a new session or switching AGY accounts:

1. **Pull Latest Code**:
   ```bash
   git pull origin main
   ```
2. **Verify System Integrity**:
   ```bash
   python test_price_scraper_integrity.py
   python check_fixes.py
   ```
3. **Run Zero-Drift Daily Health Check**:
   ```bash
   python run_daily_health_check.py
   ```
4. **Launch Web Console Server**:
   ```bash
   python -u web_console_server.py
   ```
5. **Open Admin Console**: Go to `http://localhost:5000` in your browser.

All code edits, template fixes, verification rules, and landing pages are saved in Git and deployed live on GitHub Pages!
