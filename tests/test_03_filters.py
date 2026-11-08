"""
test_03_filters.py  –  Filter Buttons
=======================================
Tests that cover the All / Active / Done filter buttons.

CONCEPTS PRACTICED:
  - Clicking buttons and checking CSS active states
  - Verifying which items are shown vs. hidden
  - Multi-step interaction flows
"""

import pytest
from selenium.webdriver.common.by import By
from tests.helpers import (
    Locators, add_task, check_task, get_todo_texts
)


class TestFilters:

    def _setup_mixed_tasks(self, driver):
        """
        Helper: add 3 tasks, complete 1.
        Returns: (active_task_1, active_task_2, done_task)
        """
        active1, active2, done = "Walk dog", "Read book", "Call mom"
        add_task(driver, active1)
        add_task(driver, active2)
        add_task(driver, done)
        check_task(driver, 2)   # mark third item (done) as complete
        return active1, active2, done

    # ---- Default filter ----

    def test_default_filter_shows_all(self, app):
        """
        On fresh load the 'All' filter button should have the 'active' class.
        """
        all_btn = app.find_element(*Locators.FILTER_ALL)
        assert "active" in all_btn.get_attribute("class")

    # ---- All filter ----

    def test_all_filter_shows_active_and_done(self, app):
        """
        'All' filter should display every task regardless of completion.
        """
        active1, active2, done = self._setup_mixed_tasks(app)
        app.find_element(*Locators.FILTER_ALL).click()

        texts = get_todo_texts(app)
        assert active1 in texts
        assert active2 in texts
        assert done    in texts

    # ---- Active filter ----

    def test_active_filter_shows_only_incomplete(self, app):
        """
        STEPS:
          1. Add mixed tasks
          2. Click 'Active' filter
          3. Assert only unchecked tasks are visible

        CONCEPT: Filtering and partial list assertions
        """
        active1, active2, done = self._setup_mixed_tasks(app)
        app.find_element(*Locators.FILTER_ACTIVE).click()

        texts = get_todo_texts(app)
        assert active1 in texts
        assert active2 in texts
        assert done    not in texts

    def test_active_filter_button_becomes_active(self, app):
        """Clicking 'Active' gives it the CSS 'active' class."""
        app.find_element(*Locators.FILTER_ACTIVE).click()
        btn = app.find_element(*Locators.FILTER_ACTIVE)
        assert "active" in btn.get_attribute("class")

    # ---- Done filter ----

    def test_done_filter_shows_only_completed(self, app):
        """
        'Done' filter should show only completed tasks.
        """
        active1, active2, done = self._setup_mixed_tasks(app)
        app.find_element(*Locators.FILTER_DONE).click()

        texts = get_todo_texts(app)
        assert done    in texts
        assert active1 not in texts
        assert active2 not in texts

    def test_done_filter_button_becomes_active(self, app):
        """Clicking 'Done' gives it the CSS 'active' class."""
        app.find_element(*Locators.FILTER_DONE).click()
        btn = app.find_element(*Locators.FILTER_DONE)
        assert "active" in btn.get_attribute("class")

    # ---- Switching filters ----

    def test_switching_from_active_to_all_shows_all(self, app):
        """
        After switching to 'Active' and back to 'All',
        all tasks should be visible again.
        """
        active1, active2, done = self._setup_mixed_tasks(app)

        app.find_element(*Locators.FILTER_ACTIVE).click()
        app.find_element(*Locators.FILTER_ALL).click()

        texts = get_todo_texts(app)
        assert active1 in texts
        assert active2 in texts
        assert done    in texts

    def test_only_one_filter_button_active_at_a_time(self, app):
        """
        Exactly one filter button should have class 'active' at any time.
        """
        app.find_element(*Locators.FILTER_ACTIVE).click()

        all_btn    = app.find_element(*Locators.FILTER_ALL)
        active_btn = app.find_element(*Locators.FILTER_ACTIVE)
        done_btn   = app.find_element(*Locators.FILTER_DONE)

        active_classes = [
            "active" in b.get_attribute("class")
            for b in [all_btn, active_btn, done_btn]
        ]
        assert sum(active_classes) == 1   # exactly one is active
