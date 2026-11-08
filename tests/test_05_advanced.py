"""
test_05_advanced.py  –  Advanced Selenium Concepts
====================================================
Covers JavaScript execution, screenshots, keyboard shortcuts,
ActionChains, and element attributes.

CONCEPTS PRACTICED:
  - execute_script (JavaScript injection)
  - ActionChains (hover, keyboard)
  - get_attribute / get_property
  - Taking screenshots
  - Reading CSS property values
"""

import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from tests.helpers import Locators, add_task, get_todo_texts


SCREENSHOTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "screenshots"
)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


class TestAdvanced:

    # ---- JavaScript Execution ----

    def test_execute_script_scroll_to_bottom(self, app):
        """
        Use JavaScript to scroll the page to the bottom.
        CONCEPT: driver.execute_script()
        """
        for i in range(10):
            add_task(app, f"Scroll task {i + 1}")

        app.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Assert we can still find the list
        todo_list = app.find_element(*Locators.TODO_LIST)
        assert todo_list.is_displayed()

    def test_execute_script_get_page_title(self, app):
        """
        Read document.title via JavaScript.
        CONCEPT: execute_script return value
        """
        title = app.execute_script("return document.title;")
        assert "Todo" in title

    def test_execute_script_check_item_count(self, app):
        """
        Count list items via JavaScript and compare with Python.
        """
        add_task(app, "JS count test A")
        add_task(app, "JS count test B")

        js_count = app.execute_script(
            "return document.querySelectorAll('#todo-list .todo-item').length;"
        )
        assert js_count >= 2

    def test_execute_script_click_button(self, app):
        """
        Click a button using JavaScript (useful for elements blocked by overlays).
        CONCEPT: execute_script to click
        """
        inp = app.find_element(*Locators.TODO_INPUT)
        inp.send_keys("JS click test")

        add_btn = app.find_element(*Locators.ADD_BUTTON)
        app.execute_script("arguments[0].click();", add_btn)

        assert "JS click test" in get_todo_texts(app)

    # ---- Screenshots ----

    def test_take_screenshot_on_state(self, app):
        """
        Save a screenshot of the current state.
        CONCEPT: save_screenshot()
        """
        add_task(app, "Screenshot task")
        path = os.path.join(SCREENSHOTS_DIR, "test_screenshot.png")
        app.save_screenshot(path)
        assert os.path.exists(path)

    # ---- Element Attributes & Properties ----

    def test_input_placeholder_text(self, app):
        """
        Read the placeholder attribute from the input field.
        CONCEPT: get_attribute()
        """
        inp = app.find_element(*Locators.TODO_INPUT)
        placeholder = inp.get_attribute("placeholder")
        assert placeholder is not None
        assert len(placeholder) > 0

    def test_input_max_length_attribute(self, app):
        """
        The input should have maxlength="100" as set in the HTML.
        """
        inp = app.find_element(*Locators.TODO_INPUT)
        maxlen = inp.get_attribute("maxlength")
        assert maxlen == "100"

    def test_add_button_is_enabled(self, app):
        """
        The Add button should always be enabled (not disabled).
        CONCEPT: is_enabled()
        """
        btn = app.find_element(*Locators.ADD_BUTTON)
        assert btn.is_enabled()

    # ---- ActionChains ----

    def test_action_chain_hover_delete_button(self, app):
        """
        Hover over a delete button and verify it's visible.
        CONCEPT: ActionChains.move_to_element()
        """
        add_task(app, "Hover me")

        delete_btn = app.find_element(By.CSS_SELECTOR, ".delete-btn")
        actions = ActionChains(app)
        actions.move_to_element(delete_btn).perform()

        assert delete_btn.is_displayed()

    def test_keyboard_tab_navigation(self, app):
        """
        Tab from the input to the Add button (keyboard navigation).
        CONCEPT: Keys.TAB via ActionChains
        """
        inp = app.find_element(*Locators.TODO_INPUT)
        inp.click()

        actions = ActionChains(app)
        actions.send_keys(Keys.TAB).perform()

        # After tabbing, focus moves to Add button; it should still be enabled
        add_btn = app.find_element(*Locators.ADD_BUTTON)
        assert add_btn.is_enabled()

    # ---- CSS Properties ----

    def test_read_css_value_of_button(self, app):
        """
        Read a CSS property (cursor) from the Add button.
        CONCEPT: value_of_css_property()
        """
        btn = app.find_element(*Locators.ADD_BUTTON)
        cursor = btn.value_of_css_property("cursor")
        assert cursor == "pointer"

    def test_todo_list_is_visible_on_load(self, app):
        """
        The todo-list <ul> should always be in the DOM.
        """
        ul = app.find_element(*Locators.TODO_LIST)
        assert ul.is_displayed()

    # ---- Parameterized-style test using plain loop ----

    def test_many_different_tasks_all_appear(self, app):
        """
        Add a variety of tasks (some with special characters) and verify.
        CONCEPT: Boundary / data-driven testing without a framework
        """
        special_tasks = [
            "Task with spaces",
            "Task123",
            "Todo: check email",
        ]
        for t in special_tasks:
            add_task(app, t)

        texts = get_todo_texts(app)
        for t in special_tasks:
            assert t in texts, f"Expected '{t}' to be in list"
