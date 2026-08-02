import sqlite3
import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "cache" / "image_cache.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_image_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS product_images (
            asin TEXT PRIMARY KEY,
            image_url TEXT NOT NULL,
            source TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Initialize DB table on import
init_image_db()

def get_cached_image(asin: str) -> str:
    """Returns permanently cached image URL for an ASIN if it exists in SQLite DB."""
    if not asin:
        return ""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT image_url FROM product_images WHERE asin = ?", (asin.upper().strip(),))
        row = c.fetchone()
        conn.close()
        return row[0] if row and row[0] else ""
    except Exception as e:
        print(f"[Image DB Error] Could not read cache for {asin}: {e}")
        return ""

def set_cached_image(asin: str, image_url: str, source: str = "discovery"):
    """Saves resolved high-res product image URL permanently into SQLite DB."""
    if not asin or not image_url or not image_url.startswith("http"):
        return
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT OR REPLACE INTO product_images (asin, image_url, source, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (asin.upper().strip(), image_url.strip(), source))
        conn.commit()
        conn.close()
        print(f"[Image DB] Saved image for {asin} -> {image_url[:60]} ({source})")
    except Exception as e:
        print(f"[Image DB Error] Could not write cache for {asin}: {e}")
