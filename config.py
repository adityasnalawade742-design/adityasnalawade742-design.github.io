import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Load .env file
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
AMAZON_ASSOCIATE_TAG = os.getenv("AMAZON_ASSOCIATE_TAG", "smartdeal0358-21")

# Multi-Key SerpAPI Support (comma-separated or SERPAPI_KEY_2, SERPAPI_KEY_3)
raw_serp_key = os.getenv("SERPAPI_KEY", "")
raw_serp_keys = os.getenv("SERPAPI_KEYS", "")
SERPAPI_KEYS = []

if raw_serp_keys:
    SERPAPI_KEYS = [k.strip() for k in raw_serp_keys.split(",") if k.strip()]
elif raw_serp_key:
    SERPAPI_KEYS = [k.strip() for k in raw_serp_key.split(",") if k.strip()]

for i in range(2, 10):
    k_extra = os.getenv(f"SERPAPI_KEY_{i}", "").strip()
    if k_extra and k_extra not in SERPAPI_KEYS:
        SERPAPI_KEYS.append(k_extra)

SERPAPI_KEY = SERPAPI_KEYS[0] if SERPAPI_KEYS else ""
RAINFOREST_API_KEY = os.getenv("RAINFOREST_API_KEY", "")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN", "")
PINTEREST_ACCESS_TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN", "")
PINTEREST_BOARD_ID = os.getenv("PINTEREST_BOARD_ID", "")
BASE_BRIDGE_URL = os.getenv("BASE_BRIDGE_URL", "https://your-app.vercel.app")
NICHE = os.getenv("NICHE", "Cozy Room & Desk Setup Decor")
OUTPUT_DIR = BASE_DIR / "output"
IMAGES_DIR = OUTPUT_DIR / "images"
BRIDGE_DIR = OUTPUT_DIR / "bridge_pages"

# Create output directories if they don't exist
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
BRIDGE_DIR.mkdir(parents=True, exist_ok=True)

if not GEMINI_API_KEY:
    print("[Config Warning] GEMINI_API_KEY is not set in .env — Gemini AI features will use fallbacks.")


