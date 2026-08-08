"""
Comprehensive Unit Test Suite for Amazon OneLink & Fallback Affiliate Routing.
Validates canonical URL generation, marketplace configuration, tag integrity, and fallback rules.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from modules.affiliate_manager import (
    build_affiliate_url,
    load_affiliate_config,
    get_canonical_tag,
    get_canonical_domain,
    is_onelink_enabled_for_country,
    get_marketplace_info
)

class TestAffiliateRouting(unittest.TestCase):

    def setUp(self):
        self.config = load_affiliate_config()

    def test_canonical_onelink_us(self):
        url = build_affiliate_url("B0DZD1X83N", marketplace="US")
        self.assertEqual(url, "https://www.amazon.com/dp/B0DZD1X83N?tag=smartdeal0358-20")
        self.assertIn("smartdeal0358-20", url)
        self.assertNotIn("smartdeal0358-21", url)

    def test_onelink_enabled_marketplaces(self):
        # US, CA, GB, DE, FR, IT, ES must be ONELINK mode
        for cc in ["US", "CA", "GB", "UK", "DE", "FR", "IT", "ES"]:
            info = get_marketplace_info(cc)
            self.assertIsNotNone(info, f"Marketplace {cc} missing from config")
            self.assertEqual(info.get("routing_mode"), "ONELINK", f"{cc} should be ONELINK mode")
            self.assertTrue(info.get("oneLink_enabled_for_account"), f"{cc} should be enabled for account")

    def test_india_direct_fallback(self):
        info = get_marketplace_info("IN")
        self.assertIsNotNone(info)
        self.assertFalse(info.get("oneLink_supported_by_amazon"))
        self.assertFalse(info.get("oneLink_enabled_for_account"))
        self.assertEqual(info.get("routing_mode"), "DIRECT_FALLBACK")
        self.assertEqual(info.get("tracking_id"), "smartdeal0358-21")
        
        # Test direct URL generation for India
        url = build_affiliate_url("B0BZXNSW5K", marketplace="IN", mode="DIRECT_FALLBACK")
        self.assertEqual(url, "https://www.amazon.in/dp/B0BZXNSW5K?tag=smartdeal0358-21")
        
        # Test search fallback URL generation for India
        search_url = build_affiliate_url("B0BZXNSW5K", marketplace="IN", mode="SEARCH_FALLBACK", keywords="Touch Bedside Lamp")
        self.assertEqual(search_url, "https://www.amazon.in/s?k=Touch+Bedside+Lamp&tag=smartdeal0358-21")

    def test_unsupported_non_onelink_marketplaces(self):
        # Non-OneLink marketplaces like JP, AU, MX, BR must be DIRECT_FALLBACK
        for cc in ["JP", "AU", "MX", "BR", "SG", "AE", "SA", "EG"]:
            info = get_marketplace_info(cc)
            if info:
                self.assertEqual(info.get("routing_mode"), "DIRECT_FALLBACK")
                self.assertFalse(info.get("oneLink_enabled_for_account"))

    def test_unknown_marketplace_safe_result(self):
        url = build_affiliate_url("B0DZD1X83N", marketplace="XYZ")
        # Should safely fall back to canonical US OneLink URL
        self.assertEqual(url, "https://www.amazon.com/dp/B0DZD1X83N?tag=smartdeal0358-20")

    def test_wrong_tag_detection(self):
        url = build_affiliate_url("B0DZD1X83N", marketplace="US")
        # India tag smartdeal0358-21 must NOT be on US URL
        self.assertNotIn("smartdeal0358-21", url)
        self.assertIn("smartdeal0358-20", url)

    def test_no_tracking_id_prevention(self):
        url = build_affiliate_url("B0DZD1X83N", marketplace="US")
        self.assertIn("tag=", url)
        self.assertTrue(len(url.split("tag=")[1]) > 0)

    def test_third_party_shortener_absence(self):
        url = build_affiliate_url("B0DZD1X83N")
        for shortener in ["shrinkme", "bit.ly", "tinyurl", "goo.gl", "ow.ly"]:
            self.assertNotIn(shortener, url.lower())

if __name__ == "__main__":
    unittest.main()
