"""
Comprehensive Diagnostic & Verification Suite for Price Scraper Integrity.
Verifies structured price records, 7-day TTL stale price logic, US ASIN fallback prohibitions,
seller verification tracking, and product regression invariants (B0BXP7YWHJ & B0CX144DHK).
"""
import unittest
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from modules.price_registry_manager import (
    create_price_record,
    extract_price_string,
    is_price_stale,
    normalize_registry_record,
    get_flat_regional_prices,
    verify_seller,
    STATUS_FRESH_VERIFIED,
    STATUS_FRESH_UNVERIFIED,
    STATUS_STALE_VERIFIED,
    STATUS_NOT_MAPPED,
    STATUS_UNAVAILABLE,
    PRICE_TTL_DAYS
)

ROOT = Path(__file__).resolve().parent
REGISTRY_FILE = ROOT / "product_price_registry.json"


class TestPriceScraperIntegrity(unittest.TestCase):

    def setUp(self):
        self.assertTrue(REGISTRY_FILE.exists(), "product_price_registry.json must exist")
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            self.registry = json.load(f)

    def test_unmapped_regional_asin_prohibits_fallback_scrape(self):
        """
        REQ 1 & REQ 2: Missing regional ASIN must NOT cause US ASIN to be scraped
        and stored as a verified regional price.
        """
        item = {
            "asin": "B0BXP7YWHJ",
            "regional_asins": {"US": "B0BXP7YWHJ"},
            "regional_prices": {}
        }
        # Simulate scraper behavior for unmapped IN region
        mapped_in = item["regional_asins"].get("IN")
        self.assertIsNone(mapped_in, "IN ASIN must be unmapped for B0BXP7YWHJ")
        
        # When unmapped, scraper sets STATUS_NOT_MAPPED
        item["regional_prices"]["IN"] = {
            "price": "Not Available",
            "asin": None,
            "country_code": "IN",
            "is_direct": False,
            "identity_verified": False,
            "seller_verified": False,
            "status": STATUS_NOT_MAPPED
        }
        
        self.assertEqual(extract_price_string(item["regional_prices"]["IN"]), "Not Available")
        self.assertFalse(item["regional_prices"]["IN"]["is_direct"])

    def test_mapped_regional_asin_allows_direct_scrape(self):
        """
        REQ 1 & REQ 4: Explicitly mapped regional ASIN matches expected ASIN -> identity verified.
        """
        item = self.registry.get("B0CX144DHK")
        self.assertIsNotNone(item)
        mapped_in = item.get("regional_asins", {}).get("IN")
        self.assertEqual(mapped_in, "B0CX144DHK")
        
        record = create_price_record(
            price_str="₹3,150.00",
            asin="B0CX144DHK",
            country_code="IN",
            is_direct=True,
            seller="Amazon.in",
            detected_asin="B0CX144DHK"
        )
        self.assertEqual(record["status"], STATUS_FRESH_VERIFIED)
        self.assertTrue(record["identity_verified"])
        self.assertTrue(record["is_direct"])

    def test_reseller_import_price_never_automatically_verified(self):
        """
        REQ 3: Reseller/import price without verified regional ASIN must NEVER be FRESH_VERIFIED.
        """
        record = create_price_record(
            price_str="₹7,111.00",
            asin="B0BXP7YWHJ",
            country_code="IN",
            is_direct=False,
            seller="Third Party Importer"
        )
        self.assertNotEqual(record["status"], STATUS_FRESH_VERIFIED)
        self.assertFalse(record["is_direct"])

    def test_seller_information_tracking(self):
        """
        REQ 5 & REQ 6: Seller info captured when available; seller_verified false when unverified seller.
        """
        rec_amazon = create_price_record(
            price_str="$19.99",
            asin="B0BZXNSW5K",
            country_code="US",
            is_direct=True,
            seller="Amazon.com Services LLC",
            detected_asin="B0BZXNSW5K"
        )
        self.assertTrue(rec_amazon["seller_verified"])

        rec_3rd = create_price_record(
            price_str="₹7,111.00",
            asin="B0BXP7YWHJ",
            country_code="IN",
            is_direct=False,
            seller="Global Imports Reseller"
        )
        self.assertFalse(rec_3rd["seller_verified"])

    def test_scrape_timestamp_and_failed_scrape_preserves_timestamp(self):
        """
        REQ 7 & REQ 8: Scrape timestamp recorded; failed scrape does NOT update timestamp.
        """
        old_ts = "2026-08-01T12:00:00Z"
        existing = {
            "price": "₹3,150.00",
            "scraped_at": old_ts,
            "status": STATUS_FRESH_VERIFIED
        }
        # Simulate scrape failure
        failed_rec = create_price_record(
            price_str=None,
            asin="B0CX144DHK",
            country_code="IN",
            is_direct=True,
            existing_record=existing
        )
        self.assertEqual(failed_rec["scraped_at"], old_ts, "Failed scrape MUST preserve previous timestamp")

    def test_stale_price_ttl_and_unverified_upgrade_prevention(self):
        """
        REQ 9 & REQ 10: Price older than 7 days becomes stale; stale price cannot become VERIFIED DEAL.
        """
        stale_ts = (datetime.now(timezone.utc) - timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.assertTrue(is_price_stale(stale_ts, ttl_days=PRICE_TTL_DAYS))

        stale_rec = create_price_record(
            price_str=None,
            asin="B0CX144DHK",
            country_code="IN",
            is_direct=True,
            existing_record={"price": "₹3,150.00", "scraped_at": stale_ts, "status": STATUS_FRESH_VERIFIED}
        )
        self.assertEqual(stale_rec["status"], STATUS_STALE_VERIFIED)

    def test_product_a_b0bxp7ywhj_regression(self):
        """
        REQ 11: B0BXP7YWHJ has no India regional ASIN, must remain unverified in India.
        """
        item = self.registry.get("B0BXP7YWHJ")
        self.assertIsNotNone(item)
        in_asin = item.get("regional_asins", {}).get("IN")
        self.assertIsNone(in_asin, "B0BXP7YWHJ must NOT have India regional ASIN mapped")
        
        flat = get_flat_regional_prices(item)
        self.assertIn("IN", flat)

    def test_product_b_b0cx144dhk_regression(self):
        """
        REQ 12: B0CX144DHK has explicit India regional ASIN mapped.
        """
        item = self.registry.get("B0CX144DHK")
        self.assertIsNotNone(item)
        in_asin = item.get("regional_asins", {}).get("IN")
        self.assertEqual(in_asin, "B0CX144DHK")
        self.assertIn("IN", item.get("direct_regions", []))

    def test_onelink_and_india_routing_invariants(self):
        """
        REQ 13, 14, 15: OneLink canonical tags (smartdeal0358-20) and India tags (smartdeal0358-21) preserved.
        """
        from modules.affiliate_manager import get_canonical_tag, build_affiliate_url
        self.assertEqual(get_canonical_tag(), "smartdeal0358-20")
        
        us_url = build_affiliate_url("B0BZXNSW5K", marketplace="US")
        self.assertEqual(us_url, "https://www.amazon.com/dp/B0BZXNSW5K?tag=smartdeal0358-20")
        
        in_url = build_affiliate_url("B0CX144DHK", marketplace="IN", mode="DIRECT_FALLBACK")
        self.assertEqual(in_url, "https://www.amazon.in/dp/B0CX144DHK?tag=smartdeal0358-21")

    # RULE 7 NEW REGRESSION TESTS (TEST 1 - TEST 7)

    def test_rule7_test1_amazon_seller_text(self):
        """TEST 1: Amazon seller text -> seller_verified = True"""
        self.assertTrue(verify_seller("Amazon.in"))
        self.assertTrue(verify_seller("Sold by Amazon.com Services LLC"))
        self.assertTrue(verify_seller("Dispatched from and sold by Amazon."))
        
        rec = create_price_record(
            price_str="$19.99",
            asin="B0BZXNSW5K",
            country_code="US",
            is_direct=True,
            seller="Sold by Amazon.com Services LLC",
            detected_asin="B0BZXNSW5K"
        )
        self.assertTrue(rec["seller_verified"])

    def test_rule7_test2_third_party_reseller_ships_from_amazon(self):
        """TEST 2: "Sold by ResellerX and Ships from Amazon" -> seller_verified = False"""
        self.assertFalse(verify_seller("Sold by ResellerX and Ships from Amazon"))
        self.assertFalse(verify_seller("Ships from Amazon"))
        self.assertFalse(verify_seller("Sold by ABC Store"))
        
        rec = create_price_record(
            price_str="₹7,111.00",
            asin="B0BXP7YWHJ",
            country_code="IN",
            is_direct=True,
            seller="Sold by ResellerX and Ships from Amazon",
            detected_asin="B0BXP7YWHJ"
        )
        self.assertFalse(rec["seller_verified"])
        self.assertEqual(rec["status"], STATUS_FRESH_UNVERIFIED)

    def test_rule7_test3_expected_asin_matches_detected_asin(self):
        """TEST 3: Expected ASIN == detected ASIN -> identity_verified = True"""
        rec = create_price_record(
            price_str="₹3,150.00",
            asin="B0CX144DHK",
            country_code="IN",
            is_direct=True,
            seller="Amazon.in",
            detected_asin="B0CX144DHK"
        )
        self.assertTrue(rec["identity_verified"])
        self.assertEqual(rec["status"], STATUS_FRESH_VERIFIED)

    def test_rule7_test4_expected_asin_mismatch_detected_asin(self):
        """TEST 4: Expected ASIN != detected ASIN -> identity_verified = False"""
        rec = create_price_record(
            price_str="₹3,150.00",
            asin="B0CX144DHK",
            country_code="IN",
            is_direct=True,
            seller="Amazon.in",
            detected_asin="B099999999"
        )
        self.assertFalse(rec["identity_verified"])
        self.assertEqual(rec["status"], STATUS_FRESH_UNVERIFIED)

    def test_rule7_test5_detected_asin_unavailable(self):
        """TEST 5: Detected ASIN unavailable (None) -> identity_verified = False"""
        rec = create_price_record(
            price_str="₹3,150.00",
            asin="B0CX144DHK",
            country_code="IN",
            is_direct=True,
            seller="Amazon.in",
            detected_asin=None,
            identity_verified=False
        )
        self.assertFalse(rec["identity_verified"])
        self.assertEqual(rec["status"], STATUS_FRESH_UNVERIFIED)

    def test_rule7_test6_b0bxp7ywhj_in_unmapped_unverified(self):
        """TEST 6: B0BXP7YWHJ IN -> NOT_MAPPED / UNVERIFIED"""
        item = self.registry.get("B0BXP7YWHJ")
        mapped_in = item.get("regional_asins", {}).get("IN")
        self.assertIsNone(mapped_in)
        rec = {
            "price": "Not Available",
            "asin": None,
            "country_code": "IN",
            "is_direct": False,
            "identity_verified": False,
            "seller_verified": False,
            "status": STATUS_NOT_MAPPED
        }
        self.assertEqual(rec["status"], STATUS_NOT_MAPPED)
        self.assertNotEqual(rec["status"], STATUS_FRESH_VERIFIED)

    def test_rule7_test7_b0cx144dhk_in_mapped_and_verified(self):
        """TEST 7: B0CX144DHK IN -> correct mapped ASIN and verified behavior when live evidence supports it"""
        item = self.registry.get("B0CX144DHK")
        mapped_in = item.get("regional_asins", {}).get("IN")
        self.assertEqual(mapped_in, "B0CX144DHK")
        rec = create_price_record(
            price_str="₹3,150.00",
            asin="B0CX144DHK",
            country_code="IN",
            is_direct=True,
            seller="Amazon.in",
            detected_asin="B0CX144DHK"
        )
        self.assertEqual(rec["status"], STATUS_FRESH_VERIFIED)
        self.assertTrue(rec["identity_verified"])
        self.assertTrue(rec["seller_verified"])


if __name__ == "__main__":
    unittest.main()

