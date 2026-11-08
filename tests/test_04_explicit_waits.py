"""
test_04_explicit_waits.py  –  Explicit Waits & Dynamic Elements
=================================================================
Demonstrates using WebDriverWait instead of implicit waits.
Best practice when dealing with async/dynamic content.

CONCEPTS PRACTICED:
  - WebDriverWait + expected_conditions (EC)
  - visibility_of_element_located
  - text_to_be_present_in_element
  - invisibility_of_element_located
  - element_to_be_clickable
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.helpers import Locators, add_task, check_task, delete_task


# How long to wait (seconds) before raising TimeoutException
WAIT_TIMEOUT = 10


class TestExplicitWaits:

    def test_wait_for_task_to_appear(self, app):
        """
        After adding a task, explicitly wait until it's visible in the DOM.

        CONCEPT: WebDriverWait + visibility_of_element_located
        """
        add_task(app, "Explicit wait task")

        # Wait until at least one .todo-item is visible
        wait = WebDriverWait(app, WAIT_TIMEOUT)
        item = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#todo-list .todo-item")
            )
        )
        assert item.is_displayed()

    def test_wait_for_error_message_text(self, app):
        """
        After triggering a validation error, wait until the error element
        contains the expected text.

        CONCEPT: text_to_be_present_in_element
        """
        # Trigger empty-input error
        app.find_element(*Locators.ADD_BUTTON).click()

        wait = WebDriverWait(app, WAIT_TIMEOUT)
        wait.until(
            EC.text_to_be_present_in_element(
                Locators.ERROR_MSG, "empty"
            )
        )

        error = app.find_element(*Locators.ERROR_MSG)
        assert "empty" in error.text.lower()

    def test_wait_for_element_to_be_clickable(self, app):
        """
        Wait until the Add button is clickable before interacting.

        CONCEPT: element_to_be_clickable
        """
        wait = WebDriverWait(app, WAIT_TIMEOUT)
        add_btn = wait.until(
            EC.element_to_be_clickable(Locators.ADD_BUTTON)
        )
        assert add_btn.is_enabled()

    def test_wait_for_item_count_text_change(self, app):
        """
        After adding a task wait until the counter text changes to '1 task'.

        CONCEPT: text_to_be_present_in_element
        """
        wait = WebDriverWait(app, WAIT_TIMEOUT)
        add_task(app, "Watch the counter")

        wait.until(
            EC.text_to_be_present_in_element(
                Locators.ITEM_COUNT, "1"
            )
        )
        count_text = app.find_element(*Locators.ITEM_COUNT).text
        assert "1" in count_text

    def test_wait_for_empty_msg_after_delete(self, app):
        """
        After deleting the only task, wait until the empty message is visible.

        CONCEPT: visibility_of_element_located after dynamic removal
        """
        add_task(app, "Temporary task")
        delete_task(app, 0)

        wait = WebDriverWait(app, WAIT_TIMEOUT)
        empty = wait.until(
            EC.visibility_of_element_located(Locators.EMPTY_MSG)
        )
        assert empty.is_displayed()

    def test_multiple_tasks_all_visible(self, app):
        """
        Add several tasks and wait until all are present.

        CONCEPT: presence_of_all_elements_located
        """
        tasks = ["First", "Second", "Third"]
        for t in tasks:
            add_task(app, t)

        wait = WebDriverWait(app, WAIT_TIMEOUT)
        items = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "#todo-list .todo-item")
            )
        )
        assert len(items) >= len(tasks)
