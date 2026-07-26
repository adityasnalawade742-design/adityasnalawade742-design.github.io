import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Load .env file
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
AMAZON_ASSOCIATE_TAG = os.getenv("AMAZON_ASSOCIATE_TAG", "smartdeal0358-21")
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")
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
    raise ValueError("GEMINI_API_KEY is not set in .env file.")

