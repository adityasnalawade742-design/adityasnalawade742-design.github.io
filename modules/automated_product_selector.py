import json
from pathlib import Path
from config import AMAZON_ASSOCIATE_TAG

PROCESSED_FILE = Path("G:/CLI/pinterest-auto-affiliate/processed_asins.json")

# Curated High-Converting Home Decor Product Pipeline ($15-$45 Impulse Price, 4.4★+ Rating)
VIRAL_HOME_DECOR_QUEUE = [
    {
        "id": "B0BQBKWSKK",
        "url": f"https://www.amazon.com/dp/B0BQBKWSKK?tag={AMAZON_ASSOCIATE_TAG}",
        "niche": "Home Fragrance & Room Decor",
        "title": "Volcano Erupting Flame Essential Oil Diffuser with Warm LED Glow",
        "target_price": "$25.99"
    },
    {
        "id": "B0FC2DV6FP",
        "url": f"https://www.amazon.com/dp/B0FC2DV6FP?tag={AMAZON_ASSOCIATE_TAG}",
        "niche": "Bedroom Wellness Decor",
        "title": "Rain Cloud Raindrop Humidifier & Relaxing Sound Machine",
        "target_price": "$33.99"
    },
    {
        "id": "B0DZFGTCLR",
        "url": f"https://www.amazon.com/dp/B0DZFGTCLR?tag={AMAZON_ASSOCIATE_TAG}",
        "niche": "Cozy Living Room Scented Decor",
        "title": "Flameless Top-Down Candle Warmer Melting Lamp with Timer",
        "target_price": "$12.99"
    },
    {
        "id": "B0FRS84KT9",
        "url": f"https://www.amazon.com/dp/B0FRS84KT9?tag={AMAZON_ASSOCIATE_TAG}",
        "niche": "Nightstand & Desk Decor",
        "title": "Acrylic Illuminated Glowing LED Note Memo Board with Wood Base",
        "target_price": "$29.99"
    },
    {
        "id": "B08HJ2M49T",
        "url": f"https://www.amazon.com/dp/B08HJ2M49T?tag={AMAZON_ASSOCIATE_TAG}",
        "niche": "Sunlight Window Decor",
        "title": "Crystal Suncatcher Prism Window Hanging Rainbow Decor",
        "target_price": "$14.99"
    },
    {
        "id": "B0B8Z7X5M1",
        "url": f"https://www.amazon.com/dp/B0B8Z7X5M1?tag={AMAZON_ASSOCIATE_TAG}",
        "niche": "Bedroom & Vanity Mirror Decor",
        "title": "Minimalist Asymmetric Wavy Body Mirror for Vanity & Bedroom",
        "target_price": "$34.99"
    }
]

def get_processed_asins() -> list:
    """Loads list of ASINs already processed from processed_asins.json."""
    if PROCESSED_FILE.exists():
        try:
            with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # Include currently deployed ASINs by default
    return ["B0BZXNSW5K", "B0DXKGL1T2", "B0D1FRDFFX", "B0D8P8CSYP"]

def save_processed_asin(asin: str):
    """Saves a newly processed ASIN to processed_asins.json."""
    processed = get_processed_asins()
    if asin not in processed:
        processed.append(asin)
        with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
            json.dump(processed, f, indent=2)
    print(f"[Automated Selector] Saved ASIN {asin} to processed history.")

def get_next_automated_product() -> dict:
    """
    Selects the next un-processed high-converting Home Decor product from the viral queue.
    """
    processed = get_processed_asins()
    for item in VIRAL_HOME_DECOR_QUEUE:
        if item["id"] not in processed:
            print(f"[Automated Selector] Selected next Home Decor product: {item['id']} - '{item['title']}' ({item['niche']})")
            return item
    
    print("[Automated Selector] All queued Home Decor products processed!")
    return None
