# Selenium Testing Practice Project 🧪

A simple **Todo List** web app designed specifically to practice **Python + Selenium WebDriver** testing.

---

## 📁 Project Structure

```
testing practice/
├── app/
│   ├── index.html          ← The web app to test
│   ├── style.css
│   └── app.js
│
├── tests/
│   ├── conftest.py         ← Pytest fixtures (WebDriver setup)
│   ├── helpers.py          ← Reusable locators & helper functions
│   ├── test_01_add_tasks.py        ← Basic Selenium: find, click, send_keys
│   ├── test_02_complete_delete.py  ← Checkboxes, deletion, CSS classes
│   ├── test_03_filters.py          ← Filter buttons, state assertions
│   ├── test_04_explicit_waits.py   ← WebDriverWait + expected_conditions
│   └── test_05_advanced.py         ← JS execution, screenshots, ActionChains
│
├── screenshots/            ← Auto-created when tests run
├── reports/                ← HTML test report (auto-created)
├── requirements.txt
└── pytest.ini
```

---

## ⚙️ Setup

### 1. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

> **Note:** `webdriver-manager` automatically downloads the correct ChromeDriver for your Chrome version. No manual setup needed!

---

## ▶️ Running Tests

### Run all tests
```bash
pytest
```

### Run a specific file
```bash
pytest tests/test_01_add_tasks.py
```

### Run a specific test
```bash
pytest tests/test_01_add_tasks.py::TestAddTasks::test_add_single_task_via_button
```

### Run headlessly (no browser window)
Open `tests/conftest.py` and uncomment:
```python
options.add_argument("--headless=new")
```

### View the HTML report
After running, open `reports/test_report.html` in your browser.

---

## 🎓 Concepts Covered

| Test File | Selenium Concepts |
|---|---|
| `test_01_add_tasks.py` | `find_element`, `send_keys`, `click`, `is_displayed`, `get_attribute` |
| `test_02_complete_delete.py` | Checkboxes, `is_selected`, CSS classes, nested element clicks |
| `test_03_filters.py` | Multi-step flows, state management, partial list assertions |
| `test_04_explicit_waits.py` | `WebDriverWait`, `expected_conditions`, `visibility_of_element_located` |
| `test_05_advanced.py` | `execute_script`, `save_screenshot`, `ActionChains`, `value_of_css_property` |

---

## 🧩 Key Patterns

### 1. Page Object Pattern (via `helpers.py`)
Locators and actions are centralized — if the HTML changes, only one file needs updating.

### 2. Fixture Scoping
- `scope="session"` driver: browser opened once for all tests (fast)
- `scope="function"` app: fresh page navigation per test (isolated)

### 3. Explicit Waits (preferred over `time.sleep`)
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.visibility_of_element_located((By.ID, "my-id")))
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---|---|
| `ChromeDriver not found` | Make sure Chrome is installed; `webdriver-manager` handles the driver |
| Tests failing due to timing | Use `WebDriverWait` instead of `time.sleep` |
| `StaleElementReferenceException` | Re-fetch elements after page updates |
| Browser not found | Ensure Google Chrome is installed on your system |
