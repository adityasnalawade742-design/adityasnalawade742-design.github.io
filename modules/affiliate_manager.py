"""
Centralized Amazon Affiliate URL Generator & OneLink Architecture Manager.

Provides single source of truth for constructing canonical OneLink affiliate URLs,
direct regional fallback URLs, search fallback URLs, and managing marketplace routing rules.
"""
import json
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config" / "affiliate_config.json"

_CONFIG_CACHE = None

def load_affiliate_config():
    """Load and return the central affiliate_config.json data."""
    global _CONFIG_CACHE
    if _CONFIG_CACHE is not None:
        return _CONFIG_CACHE

    if CONFIG_FILE.exists():
        try:
            _CONFIG_CACHE = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            return _CONFIG_CACHE
        except Exception as e:
            print(f"⚠️ Error parsing {CONFIG_FILE}: {e}")

    # Default structural fallback
    _CONFIG_CACHE = {
        "canonical": {
            "marketplace": "US",
            "country_code": "US",
            "amazon_domain": "amazon.com",
            "tracking_id": "smartdeal0358-20"
        },
        "marketplaces": {}
    }
    return _CONFIG_CACHE

def get_canonical_tag():
    """Return the canonical US OneLink associate tracking ID (smartdeal0358-20)."""
    cfg = load_affiliate_config()
    return cfg.get("canonical", {}).get("tracking_id", "smartdeal0358-20")

def get_canonical_domain():
    """Return the canonical Amazon domain (amazon.com)."""
    cfg = load_affiliate_config()
    return cfg.get("canonical", {}).get("amazon_domain", "amazon.com")

def get_marketplace_info(marketplace_or_cc):
    """Return marketplace dictionary for a given country code / marketplace name."""
    if not marketplace_or_cc:
        return None
    code = marketplace_or_cc.upper().strip()
    cfg = load_affiliate_config()
    marketplaces = cfg.get("marketplaces", {})
    return marketplaces.get(code)

def is_onelink_enabled_for_country(country_code):
    """Return True if country is configured as ONELINK for this account."""
    info = get_marketplace_info(country_code)
    if info:
        return info.get("routing_mode") == "ONELINK" and info.get("oneLink_enabled_for_account", False)
    return False

def build_affiliate_url(asin, marketplace="US", mode=None, keywords=None):
    """
    Build and return an Amazon affiliate URL.
    Modes:
      - 'ONELINK' or None for canonical marketplace (defaults to US amazon.com with smartdeal0358-20)
      - 'DIRECT_FALLBACK': Direct /dp/ link on local domain with local tracking tag
      - 'SEARCH_FALLBACK': Category /s?k= search link on local domain with local tracking tag
    """
    if not asin:
        return ""
    
    clean_asin = str(asin).strip()
    cfg = load_affiliate_config()
    canonical = cfg.get("canonical", {})
    
    target_mp = (marketplace or "US").upper().strip()
    info = get_marketplace_info(target_mp) or canonical
    
    resolved_mode = mode
    if not resolved_mode:
        resolved_mode = info.get("routing_mode", "ONELINK")
    
    # If ONELINK or US, return canonical US OneLink URL
    if resolved_mode == "ONELINK" or target_mp == "US":
        canon_domain = canonical.get("amazon_domain", "amazon.com")
        canon_tag = canonical.get("tracking_id", "smartdeal0358-20")
        return f"https://www.{canon_domain}/dp/{clean_asin}?tag={canon_tag}"
    
    # Direct Fallback (e.g. India or non-OneLink verified regional ASIN)
    domain = info.get("amazon_domain", "amazon.com")
    tag = info.get("tracking_id") or canonical.get("tracking_id", "smartdeal0358-20")
    
    if resolved_mode == "SEARCH_FALLBACK" and keywords:
        encoded_k = urllib.parse.quote_plus(str(keywords).strip())
        return f"https://www.{domain}/s?k={encoded_k}&tag={tag}"
    
    return f"https://www.{domain}/dp/{clean_asin}?tag={tag}"
