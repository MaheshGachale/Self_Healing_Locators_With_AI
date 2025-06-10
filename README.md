# Playwright Pytest Locator Auto-Fixer

This project demonstrates a simple web app for adding two numbers, tested with Playwright and pytest. If a test fails due to a locator change, an AI script (using Gemini, placeholder) can automatically fix the locator in the test code.

## Project Structure

```
Playwrite_pytest/
│
├── app/
│   ├── app.py                # Simple web app (HTML/CSS/Flask)
│   └── templates/
│       └── index.html        # HTML for the app
│
├── tests/
│   └── test_addition.py      # Playwright + pytest test
│
├── ai_fix/
│   └── locator_fixer.py      # AI code to fix locators
│
├── requirements.txt
└── README.md
```

## Usage

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   playwright install
   ```

2. **Run the Flask app:**
   ```
   python app/app.py
   ```

3. **In another terminal, run the test:**
   ```
   pytest tests/test_addition.py
   ```

4. **If the test fails due to a locator, run the AI fixer:**
   ```
   python ai_fix/locator_fixer.py
   ```
   This will auto-fix the locator using AI (Gemini placeholder).

---

**Note:** The AI locator fixer is a template and requires integration with Gemini or another LLM for real AI-powered locator suggestions. 