import pytest
from playwright.sync_api import sync_playwright

def test_addition():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_default_timeout(10000)
        page.goto("http://localhost:5000/")
        # Fill the first number
        page.fill("#lets_change_this_locator", "2")
        # Fill the second number
        page.fill("#num2", "3")
        # Click the add button
        page.click("#add-btn")

        browser.close()
