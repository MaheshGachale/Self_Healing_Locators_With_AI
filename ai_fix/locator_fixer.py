import re
import subprocess
import requests
import json
from Config.Config import Token

def run_tests():
    result = subprocess.run(
        ["pytest", "tests/test_addition.py"], capture_output=True, text=True
    )
    return result.stdout

def find_locator_error(output):
    match = re.search(r'waiting for locator\(\s*["\\']([^"\\']+)["\\']\s*\)', output, re.MULTILINE)
    if match:
        return match.group(1)
    match = re.search(r'Error:.*locator.*not found.*["\\']([#\.\w\-]+)["\\']', output)
    if match:
        return match.group(1)
    return None

def fetch_html():
    # Use Playwright to fetch the HTML of the page
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:5000/")
        html = page.content()
        browser.close()
    return html

def find_failing_line(test_code, broken_locator):
    for line in test_code.splitlines():
        if broken_locator in line:
            return line.strip()
    return None

def sanitize_locator(locator):
    # Remove backticks and surrounding quotes, and strip whitespace
    locator = locator.strip()
    if locator.startswith("`") and locator.endswith("`"):
        locator = locator[1:-1]
    if locator.startswith('"') and locator.endswith('"'):
        locator = locator[1:-1]
    if locator.startswith("'") and locator.endswith("'"):
        locator = locator[1:-1]
    # Replace inner double quotes with single quotes for Python compatibility
    locator = locator.replace('"', "'")
    return locator

def gemini_rewrite_test_code(html, test_code, gemini_api_key):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + gemini_api_key
    headers = {"Content-Type": "application/json"}
    prompt = f"""
    You are an expert in Playwright automation using Python.
    The following is the HTML of the web page under test.
    The following is the Playwright test code (Python) with comments describing the intended actions.
    Your task:
    - Analyze the comments and the HTML.
    - For each action described in the comments (e.g., # Fill the first number), ensure there is a correct Playwright action (e.g., page.fill(...)) that matches the intent and uses the correct locator from the HTML.
    - If a locator is incorrect, fix it. If an action is missing, add it. If an action is present but wrong, rewrite it.
    - Use CSS, id, class name or any locator which is allowed by playwright.
    - Return ONLY the corrected test code (no explanation, no markdown, just the Python code).
    HTML:
    {html}

    Test code:
    {test_code}
    """
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        try:
            result = response.json()
            # Gemini may return the code in a code block, so strip it if present
            code = result["candidates"][0]["content"]["parts"][0]["text"].strip()
            if code.startswith("```"):
                code = code.strip('`').split('\n', 1)[-1]
            return code
        except Exception as e:
            print("Error parsing Gemini response:", e)
            return None
    else:
        print("Gemini API error:", response.text)
        return None

def patch_test_file_with_code(new_code):
    path = "tests/test_addition.py"
    with open(path, "w") as f:
        f.write(new_code)

if __name__ == "__main__":
    # Insert your Gemini API key here
    GEMINI_API_KEY = Token

    output = run_tests()
    broken_locator = find_locator_error(output)
    if broken_locator:
        html = fetch_html()
        with open("tests/test_addition.py", "r") as f:
            test_code = f.read()
        new_code = gemini_rewrite_test_code(html, test_code, GEMINI_API_KEY)
        if new_code and new_code.strip() != test_code.strip():
            patch_test_file_with_code(new_code)
            print("Test file updated with fixing all locators.")
        else:
            print("AI did not suggest any changes or failed to return code.")
    else:
        print("No locator errors found.") 