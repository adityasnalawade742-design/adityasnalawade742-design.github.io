---
name: pinterest-api-auditor
description: >-
  Specialized auditor skill for Pinterest API v5 integration, OAuth 2.0 token management,
  board mapping, pin creation payloads, media uploads, rate limit handling, and API compliance.
  Use when testing Pinterest integration, auditing OAuth tokens, or troubleshooting pin publishing errors.
---

# 📌 Pinterest API v5 Auditor Skill (`pinterest-api-auditor`)

This skill defines the audit procedure for inspecting Pinterest API v5 endpoints, OAuth authentication tokens, board mappings, and pin publishing compliance.

---

## 🛠️ Audit Checklist & Diagnostic Procedure

### 1. OAuth 2.0 Credentials & Scopes Audit
- Verify `.env` parameters:
  - `PINTEREST_ACCESS_TOKEN`: Bearer token
  - App ID: `1596368`
  - Target Account: `@adityasnalawade0703`
- Ensure required scopes are present: `boards:read`, `boards:write`, `pins:read`, `pins:write`.

### 2. Board Mapping Audit (`pinterest_board_mapping.json`)
- Check numeric Board ID mapping for niche categories:
  - Cozy Room & Desk Setup Decor: `1092545259543920271`
- Test board resolution script:
  ```bash
  python scratch/list_pinterest_boards.py
  ```

### 3. Pin Payload Schema Audit
Validate pin creation payload structure in `modules/pinterest_publisher.py`:
```json
{
  "board_id": "1092545259543920271",
  "title": "SEO Optimized Pin Title (Max 100 chars)",
  "description": "Keyword Rich Description (Max 500 chars)",
  "link": "https://adityasnalawade742-design.github.io/bridge_B0BZXNSW5K.html",
  "media_source": {
    "source_type": "image_url",
    "url": "https://adityasnalawade742-design.github.io/focus_product_B0BZXNSW5K_hook.jpg"
  }
}
```

### 4. Destination URL & FTC Compliance Audit
- Confirm destination URL points to a live bridge page (`bridge_{asin}.html`) containing an explicit FTC affiliate disclosure:
  > *"As an Amazon Associate I earn from qualifying purchases."*
- Confirm bridge page includes footer link to `privacy-policy.html`.

### 5. Pinterest Standard Access Application Video Audit
Check compliance against `PINTEREST_OAUTH_VIDEO_SCRIPT.md` & `PINTEREST_STANDARD_ACCESS_GUIDE.md`:
1. OAuth 2.0 flow inside n8n or Python bridge.
2. Successful API execution returning `201 Created`.
3. Live board verification.
4. Bridge landing page FTC disclosure and Privacy Policy link.
