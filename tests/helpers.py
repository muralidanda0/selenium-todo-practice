"""
helpers.py  –  Reusable Page Actions
======================================
Helper functions used across multiple test files.
Keeps test files clean and avoids code duplication.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# ------------------------------------------------------------------ #
#  Locators  (single place to update if the HTML changes)             #
# ------------------------------------------------------------------ #
class Locators:
    TODO_INPUT          = (By.ID, "todo-input")
    ADD_BUTTON          = (By.ID, "add-btn")
    TODO_LIST           = (By.ID, "todo-list")
    TODO_ITEMS          = (By.CSS_SELECTOR, "#todo-list .todo-item")
    ITEM_COUNT          = (By.ID, "item-count")
    CLEAR_COMPLETED_BTN = (By.ID, "clear-completed-btn")
    EMPTY_MSG           = (By.ID, "empty-msg")
    ERROR_MSG           = (By.ID, "error-msg")
    FILTER_ALL          = (By.ID, "filter-all")
    FILTER_ACTIVE       = (By.ID, "filter-active")
    FILTER_DONE         = (By.ID, "filter-done")


# ------------------------------------------------------------------ #
#  Action Helpers                                                      #
# ------------------------------------------------------------------ #

def add_task(driver, text: str):
    """Type a task into the input and click Add Task."""
    inp = driver.find_element(*Locators.TODO_INPUT)
    inp.clear()
    inp.send_keys(text)
    driver.find_element(*Locators.ADD_BUTTON).click()


def add_task_via_enter(driver, text: str):
    """Type a task and press Enter to add it."""
    inp = driver.find_element(*Locators.TODO_INPUT)
    inp.clear()
    inp.send_keys(text)
    inp.send_keys(Keys.RETURN)


def get_todo_items(driver):
    """Return all visible todo <li> elements."""
    return driver.find_elements(*Locators.TODO_ITEMS)


def get_todo_texts(driver) -> list[str]:
    """Return text content of all visible todo items.

    Uses get_attribute("textContent") instead of .text because Selenium's
    .text can return an empty string for <label> elements in some scenarios
    (especially on first render after page load).
    """
    return [
        item.find_element(By.CSS_SELECTOR, ".todo-text")
            .get_attribute("textContent").strip()
        for item in get_todo_items(driver)
    ]


def check_task(driver, index: int):
    """Check (complete) the task at the given index."""
    items = get_todo_items(driver)
    checkbox = items[index].find_element(By.CSS_SELECTOR, ".todo-checkbox")
    checkbox.click()


def delete_task(driver, index: int):
    """Click the delete button on the task at the given index."""
    items = get_todo_items(driver)
    delete_btn = items[index].find_element(By.CSS_SELECTOR, ".delete-btn")
    delete_btn.click()
