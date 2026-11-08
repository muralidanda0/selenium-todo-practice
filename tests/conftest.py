"""
conftest.py  –  Shared Pytest Fixtures
=======================================
This file is automatically loaded by pytest before running any tests.
It provides reusable fixtures such as the WebDriver setup/teardown.
"""

import os
import urllib.parse
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# ------------------------------------------------------------------ #
#  Build the absolute path to the app HTML file                       #
#  conftest.py lives in tests/, so we go up one level to project root #
# ------------------------------------------------------------------ #
TESTS_DIR    = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TESTS_DIR)                        # one level up
APP_PATH     = os.path.join(PROJECT_ROOT, "app", "index.html")

# URL-encode the path so spaces (e.g. "testing practice") don't break it
_posix_path = APP_PATH.replace(os.sep, "/")
APP_URL     = "file:///" + urllib.parse.quote(_posix_path, safe=":/")


# ------------------------------------------------------------------ #
#  Session-scoped driver: created once, reused across all tests       #
# ------------------------------------------------------------------ #
@pytest.fixture(scope="session")
def driver():
    """
    Creates a Chrome WebDriver instance for the test session.

    scope="session" means the browser is opened once and shared
    across all tests → faster than opening/closing per test.
    """
    options = Options()
    options.add_argument("--start-maximized")
    # Uncomment the next line to run tests headlessly (no visible browser):
    # options.add_argument("--headless=new")

    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    drv.implicitly_wait(5)   # wait up to 5 s for elements to appear

    yield drv                # hand the driver to each test

    drv.quit()               # teardown – close browser when all tests done


# ------------------------------------------------------------------ #
#  Function-scoped helper that navigates to a fresh page              #
# ------------------------------------------------------------------ #
@pytest.fixture
def app(driver):
    """
    Navigates to the Todo App and returns the driver.
    This fixture runs before every single test function,
    ensuring each test starts with a clean page load.
    """
    driver.get(APP_URL)
    return driver
