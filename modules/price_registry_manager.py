"""
Centralized Price Registry Data Manager & Integrity Verification Engine.

Manages structured price records, freshness timestamps (7-day TTL), seller verification,
and backward-compatible normalization for product_price_registry.json.
"""
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

PRICE_TTL_DAYS = 7

# Safe Status Definitions
STATUS_FRESH_VERIFIED = "FRESH_VERIFIED"
STATUS_FRESH_UNVERIFIED = "FRESH_UNVERIFIED"
STATUS_STALE_VERIFIED = "STALE_VERIFIED"
STATUS_STALE_UNVERIFIED = "STALE_UNVERIFIED"
STATUS_NOT_MAPPED = "NOT_MAPPED"
STATUS_UNAVAILABLE = "UNAVAILABLE"
STATUS_SCRAPE_FAILED = "SCRAPE_FAILED"
STATUS_LEGACY_UNVERIFIED = "LEGACY_UNVERIFIED"
STATUS_LEGACY_VERIFIED = "LEGACY_VERIFIED"


def get_now_iso() -> str:
    """Return current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso_timestamp(ts_str: str):
    """Parses ISO timestamp string into datetime object."""
    if not ts_str:
        return None
    try:
        if ts_str.endswith("Z"):
            ts_str = ts_str[:-1] + "+00:00"
        return datetime.fromisoformat(ts_str)
    except Exception:
        return None


def is_price_stale(scraped_at_str: str, ttl_days: int = PRICE_TTL_DAYS) -> bool:
    """Return True if scraped_at timestamp is older than ttl_days."""
    dt = parse_iso_timestamp(scraped_at_str)
    if not dt:
        return True
    now = datetime.now(timezone.utc)
    return (now - dt) > timedelta(days=ttl_days)


def extract_price_string(entry) -> str:
    """
    Safely extracts price string from either a legacy string or a structured dict.
    Returns string like '$19.99' or '₹3,150.00' or 'Not Available'.
    """
    if isinstance(entry, dict):
        return entry.get("price") or "Not Available"
    if isinstance(entry, str):
        return entry
    return "Not Available"


def create_price_record(
    price_str: str,
    asin: str,
    country_code: str,
    is_direct: bool = False,
    seller: str = None,
    ships_from: str = None,
    source_url: str = None,
    existing_record: dict = None
) -> dict:
    """
    Constructs a structured price record.
    If scraping failed (price_str is None or 'Not Available'), preserves existing timestamp.
    """
    now_str = get_now_iso()
    
    if not price_str or price_str == "Not Available":
        # Scrape failed or item unavailable
        if existing_record and isinstance(existing_record, dict):
            prev_ts = existing_record.get("scraped_at")
            is_stale = is_price_stale(prev_ts)
            prev_status = existing_record.get("status", STATUS_UNAVAILABLE)
            new_status = STATUS_STALE_VERIFIED if (is_stale and "VERIFIED" in prev_status) else STATUS_UNAVAILABLE
            return {
                "price": existing_record.get("price", "Not Available"),
                "asin": asin,
                "country_code": country_code,
                "is_direct": is_direct,
                "identity_verified": is_direct,
                "seller_verified": existing_record.get("seller_verified", False),
                "seller": existing_record.get("seller"),
                "ships_from": existing_record.get("ships_from"),
                "source_url": source_url or existing_record.get("source_url"),
                "scraped_at": prev_ts or now_str,
                "status": new_status
            }
        else:
            return {
                "price": "Not Available",
                "asin": asin,
                "country_code": country_code,
                "is_direct": is_direct,
                "identity_verified": is_direct,
                "seller_verified": False,
                "seller": seller,
                "ships_from": ships_from,
                "source_url": source_url,
                "scraped_at": now_str,
                "status": STATUS_UNAVAILABLE
            }

    # Fresh price extracted
    seller_clean = (seller or "").strip()
    is_amazon_seller = "amazon" in seller_clean.lower() if seller_clean else False
    seller_verified = is_direct and (is_amazon_seller or country_code in ["US"])
    status = STATUS_FRESH_VERIFIED if (is_direct and seller_verified) else (STATUS_FRESH_VERIFIED if is_direct else STATUS_FRESH_UNVERIFIED)

    return {
        "price": price_str,
        "asin": asin,
        "country_code": country_code,
        "is_direct": is_direct,
        "identity_verified": is_direct,
        "seller_verified": seller_verified,
        "seller": seller_clean or None,
        "ships_from": ships_from or None,
        "source_url": source_url,
        "scraped_at": now_str,
        "status": status
    }


def normalize_registry_record(product_item: dict) -> dict:
    """
    Safely normalizes legacy flat string prices in a product item to structured dicts
    without data corruption or false verification upgrades.
    """
    if "regional_prices" not in product_item or not isinstance(product_item["regional_prices"], dict):
        product_item["regional_prices"] = {}
        
    regional_asins = product_item.get("regional_asins", {})
    if not isinstance(regional_asins, dict):
        regional_asins = {}

    norm_prices = {}
    for cc, val in product_item["regional_prices"].items():
        if isinstance(val, dict):
            # Already structured record
            norm_prices[cc] = val
        else:
            # Legacy string price conversion
            price_str = str(val)
            mapped_asin = regional_asins.get(cc)
            is_direct = bool(mapped_asin and (cc == "US" or mapped_asin != product_item.get("asin")))
            if cc == "US":
                is_direct = True

            status = STATUS_LEGACY_VERIFIED if is_direct else STATUS_LEGACY_UNVERIFIED
            norm_prices[cc] = {
                "price": price_str,
                "asin": mapped_asin or (product_item.get("asin") if cc == "US" else None),
                "country_code": cc,
                "is_direct": is_direct,
                "identity_verified": is_direct,
                "seller_verified": is_direct,
                "seller": None,
                "ships_from": None,
                "source_url": None,
                "scraped_at": None,  # Legacy records lack timestamp
                "status": status
            }

    product_item["regional_prices"] = norm_prices
    return product_item


def get_flat_regional_prices(product_item: dict) -> dict:
    """
    Returns a flat {CC: "PriceString"} dictionary from structured or legacy regional_prices,
    ensuring 100% backward compatibility for Jinja2 templates and legacy price readers.
    """
    if "regional_prices" not in product_item or not isinstance(product_item["regional_prices"], dict):
        return {}

    flat = {}
    for cc, val in product_item["regional_prices"].items():
        flat[cc] = extract_price_string(val)
    return flat
