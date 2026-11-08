"""
test_01_add_tasks.py  –  Adding Tasks
=======================================
Tests that cover adding tasks via the button and Enter key,
empty-input validation, and duplicate detection.

CONCEPTS PRACTICED:
  - find_element / find_elements
  - send_keys, click
  - Assertions on text content
  - Implicit waits
"""

import pytest
from selenium.webdriver.common.by import By
from tests.helpers import (
    Locators, add_task, add_task_via_enter, get_todo_texts
)


class TestAddTasks:
    """Group related tests inside a class (optional but organises output)."""

    def test_page_title_is_correct(self, app):
        """The browser tab title should contain 'Todo App'."""
        assert "Todo App" in app.title

    def test_app_heading_visible(self, app):
        """The H1 heading should be visible on page load."""
        heading = app.find_element(By.ID, "app-title")
        assert heading.is_displayed()
        assert "Todo" in heading.text

    def test_add_single_task_via_button(self, app):
        """
        STEPS:
          1. Type a task name in the input
          2. Click the 'Add Task' button
          3. Assert the task appears in the list
        """
        add_task(app, "Buy groceries")
        texts = get_todo_texts(app)
        assert "Buy groceries" in texts

    def test_add_task_via_enter_key(self, app):
        """
        Pressing Enter should work the same as clicking Add Task.
        CONCEPT: send_keys(Keys.RETURN)
        """
        add_task_via_enter(app, "Learn Selenium")
        texts = get_todo_texts(app)
        assert "Learn Selenium" in texts

    def test_input_is_cleared_after_adding(self, app):
        """After a task is added, the text input should be empty."""
        add_task(app, "Walk the dog")
        inp = app.find_element(*Locators.TODO_INPUT)
        assert inp.get_attribute("value") == ""

    def test_add_multiple_tasks(self, app):
        """Add several tasks and verify they all appear."""
        tasks = ["Task Alpha", "Task Beta", "Task Gamma"]
        for t in tasks:
            add_task(app, t)

        texts = get_todo_texts(app)
        for t in tasks:
            assert t in texts

    def test_empty_input_shows_error(self, app):
        """
        Clicking Add with an empty input should show an error message.
        CONCEPT: Checking element visibility and text
        """
        # Click without typing anything
        app.find_element(*Locators.ADD_BUTTON).click()

        error = app.find_element(*Locators.ERROR_MSG)
        assert error.is_displayed()
        assert "empty" in error.text.lower()

    def test_whitespace_only_input_shows_error(self, app):
        """Spaces-only input should be treated as empty."""
        inp = app.find_element(*Locators.TODO_INPUT)
        inp.send_keys("     ")
        app.find_element(*Locators.ADD_BUTTON).click()

        error = app.find_element(*Locators.ERROR_MSG)
        assert error.is_displayed()

    def test_duplicate_task_shows_error(self, app):
        """
        Adding the same task twice should display a duplicate error.
        CONCEPT: State-dependent validation testing
        """
        add_task(app, "Unique Task")
        add_task(app, "Unique Task")   # second time → error

        error = app.find_element(*Locators.ERROR_MSG)
        assert error.is_displayed()
        assert "already exists" in error.text.lower()

    def test_item_count_updates_after_add(self, app):
        """
        The footer counter should reflect how many active tasks exist.
        CONCEPT: Reading and parsing element text
        """
        add_task(app, "Count me in")
        count_text = app.find_element(*Locators.ITEM_COUNT).text
        # e.g. "1 task remaining"
        assert "1" in count_text
