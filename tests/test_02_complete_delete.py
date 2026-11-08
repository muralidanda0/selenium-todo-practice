"""
test_02_complete_delete.py  –  Completing & Deleting Tasks
============================================================
Tests that cover marking tasks as done and removing them.

CONCEPTS PRACTICED:
  - Interacting with checkboxes
  - CSS class assertions
  - Dynamic list re-rendering
  - Element staleness awareness
"""

import pytest
from selenium.webdriver.common.by import By
from tests.helpers import (
    Locators, add_task, check_task, delete_task,
    get_todo_items, get_todo_texts
)


class TestCompleteAndDelete:

    # ---- Complete (checkbox) ----

    def test_check_task_marks_it_completed(self, app):
        """
        STEPS:
          1. Add a task
          2. Click its checkbox
          3. Assert the item has the CSS class 'completed'

        CONCEPT: get_attribute("class") / is_selected()
        """
        add_task(app, "Finish report")
        check_task(app, 0)   # check first (index 0) item

        items = get_todo_items(app)
        assert "completed" in items[0].get_attribute("class")

    def test_checkbox_is_checked_after_click(self, app):
        """
        The checkbox input's checked state should be True after clicking.
        CONCEPT: is_selected()
        """
        add_task(app, "Read a book")
        check_task(app, 0)

        items = get_todo_items(app)
        cb = items[0].find_element(By.CSS_SELECTOR, ".todo-checkbox")
        assert cb.is_selected()

    def test_uncheck_task_removes_completed_class(self, app):
        """
        Clicking the checkbox again (uncheck) should remove 'completed'.
        CONCEPT: Toggle / state round-trip
        """
        add_task(app, "Toggle me")
        check_task(app, 0)   # check
        check_task(app, 0)   # uncheck

        items = get_todo_items(app)
        assert "completed" not in items[0].get_attribute("class")

    def test_item_count_decrements_on_complete(self, app):
        """
        Completing a task should reduce the 'remaining' counter.
        """
        add_task(app, "Task one")
        add_task(app, "Task two")

        before = app.find_element(*Locators.ITEM_COUNT).text   # "2 tasks remaining"
        check_task(app, 0)
        after  = app.find_element(*Locators.ITEM_COUNT).text   # "1 task remaining"

        assert before != after
        assert "1" in after

    # ---- Delete ----

    def test_delete_removes_task_from_list(self, app):
        """
        STEPS:
          1. Add a task
          2. Click its ✕ button
          3. Assert it's gone from the list

        CONCEPT: Clicking nested child elements
        """
        add_task(app, "Delete me")
        assert "Delete me" in get_todo_texts(app)

        delete_task(app, 0)
        assert "Delete me" not in get_todo_texts(app)

    def test_delete_correct_item_from_multiple(self, app):
        """
        When multiple tasks exist, deleting one should leave others intact.
        """
        add_task(app, "Keep A")
        add_task(app, "Remove B")
        add_task(app, "Keep C")

        # Delete the SECOND item (index 1)
        delete_task(app, 1)

        remaining = get_todo_texts(app)
        assert "Remove B" not in remaining
        assert "Keep A"   in remaining
        assert "Keep C"   in remaining

    def test_list_is_empty_after_deleting_all(self, app):
        """
        After all tasks are deleted the empty message should show.
        """
        add_task(app, "Solo task")
        delete_task(app, 0)

        empty = app.find_element(*Locators.EMPTY_MSG)
        assert empty.is_displayed()

    # ---- Clear Completed ----

    def test_clear_completed_removes_done_tasks(self, app):
        """
        STEPS:
          1. Add two tasks
          2. Complete one
          3. Click 'Clear Completed'
          4. Assert only the active task remains

        CONCEPT: Combining multiple interactions
        """
        add_task(app, "Active task")
        add_task(app, "Done task")

        check_task(app, 1)   # mark "Done task" as complete

        app.find_element(*Locators.CLEAR_COMPLETED_BTN).click()

        texts = get_todo_texts(app)
        assert "Done task"   not in texts
        assert "Active task" in texts

    def test_clear_completed_button_keeps_active_tasks(self, app):
        """
        'Clear Completed' should NOT remove active (unchecked) tasks.
        """
        add_task(app, "Stay here")
        app.find_element(*Locators.CLEAR_COMPLETED_BTN).click()

        texts = get_todo_texts(app)
        assert "Stay here" in texts
