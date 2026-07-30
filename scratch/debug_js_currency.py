import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.on("console", lambda msg: print(f"Browser Console: {msg.text}"))
    page.on("pageerror", lambda err: print(f"Browser Error: {err}"))

    page.goto("file:///G:/CLI/pinterest-auto-affiliate/index.html")
    time.sleep(1)

    print("Evaluating changeGlobalCurrency('INR')...")
    res = page.evaluate("() => { changeGlobalCurrency('INR'); return document.querySelector('#card-B0GYDXHF4G .card-price-tag').innerText; }")
    print(f"Result for Diffuser: '{res}'")

    browser.close()
