---
name: n8n-workflow-auditor
description: >-
  Specialized auditor skill for n8n workflow node execution, webhook security, Replicate Flux Dev
  Img2Img prompt strength caps, Flask proxy routing on Port 5000, and workflow execution logging.
  Use when debugging n8n nodes, testing webhooks, or troubleshooting automated pipeline runs.
---

# ⚡ n8n Workflow Auditor Skill (`n8n-workflow-auditor`)

This skill defines the diagnostic protocol for auditing n8n workflow execution nodes, webhook triggers, local Flask proxy endpoints (`web_console_server.py`), and task execution logs.

---

## 🛠️ Audit Checklist & Diagnostics

### 1. Workflow JSON Schema & Node Integrity
- Inspect `fixed_n8n_workflow.json` & `n8n_pinterest_affiliate_workflow.json`.
- Verify node sequence (Nodes 1–8):
  - Node 1: Webhook Trigger (`http://localhost:5678/webhook/...`)
  - Node 2: JS Sanitizer (truncates titles to max 35 chars)
  - Node 3: Cutout vs Lifestyle Image Classifier
  - Node 4: Prompt Setters (Cutout `0.78` vs Lifestyle `0.50`)
  - Node 5: Replicate API (`black-forest-labs/flux-dev`)
  - Node 6: HTTP Request to Flask Server (`http://localhost:5000/api/create_bridge_page`)
  - Node 7: Pinterest API v5 Post Node
  - Node 8: Campaign Tracker Logger (`pinterest_campaign_tracker.json`)

### 2. Prompt Strength Cap Audit
- Confirm lifestyle room photos use `prompt_strength <= 0.55` (prevents AI hallucinated extra props).
- Confirm multi-pack / item sets use `prompt_strength = 0.28`.

### 3. Flask Server Proxy Audit (`web_console_server.py`)
- Test endpoint health on Port 5000:
  ```bash
  python scratch/test_all_endpoints.py
  python scratch/test_live_api.py
  ```
- Verify `ADMIN_SECRET_KEY` authentication for remote cloud webhooks.

### 4. Campaign Execution Logs Audit
- Inspect `pinterest_campaign_tracker.json` to verify successful executions and Pin IDs.
