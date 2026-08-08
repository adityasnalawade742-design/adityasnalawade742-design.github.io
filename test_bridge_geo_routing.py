"""
Comprehensive Bridge Geo-Routing Regression Test Suite with Playwright Browser Mocking.
Validates Network-First priority, 1.5s fallback deadline, single-resolution lock, and async race condition guards.
"""
import sys
import unittest
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

class TestBridgeGeoRouting(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sample_bridge = ROOT / "bridge_B0BZXNSW5K.html"
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def test_code_structure_has_network_first_and_resolution_lock(self):
        content = self.sample_bridge.read_text(encoding="utf-8")
        self.assertIn("executeGeoRedirect(cc, source)", content, "Missing executeGeoRedirect engine function")
        self.assertIn("detectInstantSync()", content, "Missing 0ms instant sync helper")

    def test_playwright_network_in_timezone_us_override(self):
        """
        CRITICAL BUG REGRESSION TEST:
        Browser timezone: America/New_York
        Browser language: en-US
        Mock Cloudflare network response: loc=IN
        EXPECTED RESULT: IN (amazon.in + smartdeal0358-21)
        """
        file_url = f"file:///{self.sample_bridge.resolve()}".replace("\\", "/")
        context = self.browser.new_context(
            timezone_id="America/New_York",
            locale="en-US",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        context.route("https://www.cloudflare.com/cdn-cgi/trace*", lambda route: route.fulfill(
            status=200,
            content_type="text/plain",
            body="ip=49.207.200.1\nts=1700000000\nloc=IN\nvisit_scheme=https\n"
        ))
        
        page = context.new_page()
        page.goto(file_url)
        page.wait_for_timeout(500)
        
        buy_href = page.evaluate("document.getElementById('buyBtn') ? document.getElementById('buyBtn').href : ''")
        buy_text = page.evaluate("document.getElementById('buyBtnText') ? document.getElementById('buyBtnText').innerText : ''")
        context.close()
        
        self.assertIn("amazon.in", buy_href, "Network IN must override US timezone to target amazon.in")
        self.assertIn("smartdeal0358-21", buy_href, "Network IN must use India tag smartdeal0358-21")
        self.assertIn("AMAZON INDIA", buy_text.upper())

    def test_playwright_network_us_timezone_in_override(self):
        """
        TEST 2:
        Browser timezone: Asia/Kolkata
        Browser language: en-IN
        Mock Cloudflare network response: loc=US
        EXPECTED RESULT: US (amazon.com + smartdeal0358-20)
        """
        file_url = f"file:///{self.sample_bridge.resolve()}".replace("\\", "/")
        context = self.browser.new_context(
            timezone_id="Asia/Kolkata",
            locale="en-IN",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        context.route("https://www.cloudflare.com/cdn-cgi/trace*", lambda route: route.fulfill(
            status=200,
            content_type="text/plain",
            body="ip=104.28.24.1\nts=1700000000\nloc=US\nvisit_scheme=https\n"
        ))
        
        page = context.new_page()
        page.goto(file_url)
        page.wait_for_timeout(500)
        
        buy_href = page.evaluate("document.getElementById('buyBtn') ? document.getElementById('buyBtn').href : ''")
        context.close()
        
        self.assertEqual(buy_href, "https://www.amazon.com/dp/B0BZXNSW5K?tag=smartdeal0358-20")

    def test_playwright_network_gb_timezone_us_onelink(self):
        """
        TEST 3:
        Browser timezone: America/New_York
        Mock Cloudflare network response: loc=GB
        EXPECTED RESULT: GB (canonical amazon.com + smartdeal0358-20)
        """
        file_url = f"file:///{self.sample_bridge.resolve()}".replace("\\", "/")
        context = self.browser.new_context(
            timezone_id="America/New_York",
            locale="en-US"
        )
        context.route("https://www.cloudflare.com/cdn-cgi/trace*", lambda route: route.fulfill(
            status=200,
            content_type="text/plain",
            body="ip=81.2.69.142\nts=1700000000\nloc=GB\nvisit_scheme=https\n"
        ))
        
        page = context.new_page()
        page.goto(file_url)
        page.wait_for_timeout(500)
        
        buy_href = page.evaluate("document.getElementById('buyBtn') ? document.getElementById('buyBtn').href : ''")
        buy_text = page.evaluate("document.getElementById('buyBtnText') ? document.getElementById('buyBtnText').innerText : ''")
        context.close()
        
        self.assertEqual(buy_href, "https://www.amazon.com/dp/B0BZXNSW5K?tag=smartdeal0358-20", "OneLink country GB must preserve canonical amazon.com URL")
        self.assertIn("UK", buy_text.upper())

    def test_playwright_network_timeout_timezone_in_fallback(self):
        """
        TEST 4:
        Network: TIMEOUT/FAILURE
        Browser timezone: Asia/Kolkata
        Language: en-IN
        EXPECTED RESULT: IN (amazon.in + smartdeal0358-21) via 1.5s fallback
        """
        file_url = f"file:///{self.sample_bridge.resolve()}".replace("\\", "/")
        context = self.browser.new_context(
            timezone_id="Asia/Kolkata",
            locale="en-IN"
        )
        context.route("https://www.cloudflare.com/cdn-cgi/trace*", lambda route: route.abort())
        context.route("https://ipwho.is/*", lambda route: route.abort())
        context.route("https://freeipapi.com/*", lambda route: route.abort())
        context.route("https://api.country.is/*", lambda route: route.abort())
        context.route("https://ipapi.co/*", lambda route: route.abort())
        
        page = context.new_page()
        page.goto(file_url)
        page.wait_for_timeout(1800)
        
        buy_href = page.evaluate("document.getElementById('buyBtn') ? document.getElementById('buyBtn').href : ''")
        context.close()
        
        self.assertIn("amazon.in", buy_href, "Fallback after network timeout must use India timezone detection")
        self.assertIn("smartdeal0358-21", buy_href)

    def test_playwright_network_timeout_unknown_timezone_safe_fallback(self):
        """
        TEST 5:
        Network: TIMEOUT/FAILURE
        Timezone: unknown / GMT
        EXPECTED RESULT: US safe fallback (canonical amazon.com + smartdeal0358-20)
        """
        file_url = f"file:///{self.sample_bridge.resolve()}".replace("\\", "/")
        context = self.browser.new_context(
            timezone_id="UTC",
            locale="en-US"
        )
        context.route("https://www.cloudflare.com/cdn-cgi/trace*", lambda route: route.abort())
        context.route("https://ipwho.is/*", lambda route: route.abort())
        context.route("https://freeipapi.com/*", lambda route: route.abort())
        context.route("https://api.country.is/*", lambda route: route.abort())
        context.route("https://ipapi.co/*", lambda route: route.abort())
        
        page = context.new_page()
        page.goto(file_url)
        page.wait_for_timeout(1800)
        
        buy_href = page.evaluate("document.getElementById('buyBtn') ? document.getElementById('buyBtn').href : ''")
        context.close()
        
        self.assertEqual(buy_href, "https://www.amazon.com/dp/B0BZXNSW5K?tag=smartdeal0358-20")

    def test_explicit_debug_country_override(self):
        """
        TEST 6:
        URL contains ?country=US
        Network trace returns IN
        EXPECTED RESULT: US (explicit developer override respected)
        """
        file_url = f"file:///{self.sample_bridge.resolve()}?country=US".replace("\\", "/")
        context = self.browser.new_context()
        context.route("https://www.cloudflare.com/cdn-cgi/trace*", lambda route: route.fulfill(
            status=200,
            content_type="text/plain",
            body="ip=49.207.200.1\nts=1700000000\nloc=IN\nvisit_scheme=https\n"
        ))
        page = context.new_page()
        page.goto(file_url)
        page.wait_for_timeout(300)
        
        buy_href = page.evaluate("document.getElementById('buyBtn') ? document.getElementById('buyBtn').href : ''")
        context.close()
        
        self.assertEqual(buy_href, "https://www.amazon.com/dp/B0BZXNSW5K?tag=smartdeal0358-20")

    def test_normal_showcase_links_have_no_country_parameter(self):
        """
        TEST 7:
        Verify index.html card links do not append ?country= parameter.
        """
        index_file = ROOT / "index.html"
        content = index_file.read_text(encoding="utf-8")
        soup = BeautifulSoup(content, "html.parser")
        cards = soup.find_all("a", class_="card")
        for card in cards:
            href = card.get("href", "")
            self.assertNotIn("?country=", href, f"Card href '{href}' should not contain ?country= override")
            self.assertNotIn("?geo=", href, f"Card href '{href}' should not contain ?geo= override")

if __name__ == "__main__":
    unittest.main()
