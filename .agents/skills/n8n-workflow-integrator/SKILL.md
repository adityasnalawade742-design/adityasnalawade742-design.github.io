---
name: n8n-workflow-integrator
description: >-
  Runbook for configuring, testing, and troubleshooting n8n webhook nodes (8-node pipeline in fixed_n8n_workflow.json),
  handling Replicate Flux Dev Img2Img prompt strength caps, proxying via web_console_server.py on Port 5000,
  and recording Pinterest API v5 OAuth demo scripts. Use when modifying n8n nodes, updating API webhooks,
  or preparing Pinterest Standard Access application videos.
---

# ⚡ n8n Workflow Integration & API Compliance Skill

This skill defines the operational configuration, API endpoints, and compliance guides for the 8-node **n8n Pinterest Affiliate Automation Workflow** (`fixed_n8n_workflow.json`) and local proxy server (`web_console_server.py`).

---

## 🤖 8-Node Workflow Architecture

```
[Node 1: Webhook] ➔ [Node 2: Sanitizer] ➔ [Node 3: Classifier (If Cutout)]
                                                    │
                 ┌──────────────────────────────────┴──────────────────────────────────┐
                 ▼                                                                     ▼
[Node 4A: Cutout Prompt Set] (0.78 Strength)                         [Node 4B: Lifestyle Prompt Set] (0.50 Strength)
                 │                                                                     │
                 └──────────────────────────────────┬──────────────────────────────────┘
                                                    ▼
                                     [Node 5: Replicate API (Flux Dev)]
                                                    │
                                                    ▼
                                     [Node 6: Flask Bridge & Playwright Build]
                                                    │
                                                    ▼
                                     [Node 7: Pinterest API v5 Post]
                                                    │
                                                    ▼
                                     [Node 8: Log Campaign Result]
```

### Node Functions & API Rules:
1. **Node 1 (Webhook)**: Receives JSON trigger payload from Web Console or automated scheduler.
2. **Node 2 (Sanitizer)**: JS code node truncating titles to max 35 characters and sanitizing price strings.
3. **Node 3 (Classifier)**: Evaluates image background (plain white studio cutout vs existing room scene).
4. **Node 4 (Set Prompts)**: Configures Img2Img prompt strength:
   - **Cutout Prompt (4A)**: `prompt_strength = 0.75 - 0.80` (synthesizes new room background from scratch).
   - **Lifestyle Prompt (4B)**: `prompt_strength = 0.28 - 0.55` (**CAPPED AT MAX 0.55** to prevent hallucinating extra props).
5. **Node 5 (Replicate API)**: Executes Img2Img generation using `black-forest-labs/flux-dev`.
6. **Node 6 (Flask Server Build)**: Sends POST request to `http://localhost:5000/api/create_bridge_page`.
7. **Node 7 (Pinterest API v5)**: Posts pin payload to board `1092545259543920271` via OAuth Header Auth.
8. **Node 8 (Log Result)**: Saves execution response in `pinterest_campaign_tracker.json`.

---

## 🌐 Web Console Proxy Endpoints (`web_console_server.py`)

Start the multi-threaded Flask proxy server:
```bash
python web_console_server.py
```
- Server URL: `http://localhost:5000`
- Key API Endpoints:
  - `POST /api/create_bridge_page`: Called by n8n Node 6 to build Jinja2 landing pages and invoke Playwright overlays.
  - `GET /api/batch_extract`: Scrapes Amazon product details and lifestyle images.
  - `POST /api/proxy_n8n`: Forwards requests directly to n8n webhook (`http://localhost:5678/webhook/...`).
  - `POST /api/delete_product`: Executes clean campaign deletion.

---

## 📹 Pinterest API v5 Standard Access Application Guide

To obtain Pinterest API v5 Standard Access approval, follow the 60–90 second screen capture runbook (`PINTEREST_OAUTH_VIDEO_SCRIPT.md` & `PINTEREST_STANDARD_ACCESS_GUIDE.md`):

1. Show authenticated account (`@adityasnalawade0703`).
2. Demonstrate n8n OAuth 2.0 credential node connection.
3. Execute workflow producing a live `201 Created` API response.
4. Open Pinterest and confirm pin published to board `1092545259543920271`.
5. Click pin destination link to navigate to bridge landing page (`bridge_{asin}.html`).
6. Scroll down to show FTC Affiliate Disclosure and Privacy Policy link (`privacy-policy.html`).
