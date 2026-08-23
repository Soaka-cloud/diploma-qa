from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class BoardPage(BasePage):
    ADD_TASK_BUTTON = (By.XPATH, "//*[contains(text(), 'Добавить задачу')]")
    NAME_INPUT = (By.XPATH, "//*[@data-testid='board-task-input-name']")
    EDITOR = (By.XPATH, "//*[@contenteditable='true']")
    TAB_MENU = (By.XPATH, "//*[@data-testid='board-tab-menu']")
    COLUMN_ITEM = (By.XPATH, "//*[contains(text(), 'Создать колонку')]")
    COLUMN_INPUT = (
        By.XPATH, "//textarea[@placeholder='Введите имя колонки…']",
    )

    def create_column(self, title: str) -> None:
        tab = self.wait.until(EC.element_to_be_clickable(self.TAB_MENU))
        self.driver.execute_script("arguments[0].click();", tab)
        item = self.wait.until(EC.visibility_of_element_located(
            self.COLUMN_ITEM))
        self.driver.execute_script("arguments[0].click();", item)
        self.type_text(*self.COLUMN_INPUT, title)
        self.press_enter(*self.COLUMN_INPUT)
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

    def create_task(self, name: str) -> None:
        self.is_visible(By.XPATH, "//*[@data-testid='board-column']")
        self.click(*self.ADD_TASK_BUTTON)
        self.type_text(*self.NAME_INPUT, name)
        self.press_enter(*self.NAME_INPUT)

    def is_task_visible(self, name: str) -> bool:
        locator = (
            By.XPATH,
            f"//*[@data-testid='board-task-card'][contains(., '{name}')]",
        )
        return self.is_visible(*locator)

    def move_task(self, name: str, column_title: str) -> None:
        card = self.find(
            By.XPATH,
            f"//*[@data-testid='board-task-card'][contains(., '{name}')]",
        )
        column = self.find(
            By.XPATH,
            f"//*[@data-testid='board-column'][contains(., '{column_title}')]",
        )
        target = column.find_element(
            By.XPATH, ".//*[contains(@class, 'task-group-wrap')]",
        )
        ActionChains(self.driver) \
            .click_and_hold(card) \
            .pause(0.5) \
            .move_to_element(target) \
            .pause(0.5) \
            .release() \
            .perform()

    def is_task_in_column(self, name: str, column_title: str) -> bool:
        locator = (
            By.XPATH,
            f"//*[@data-testid='board-column'][contains(., '{column_title}')]"
            f"[.//*[contains(text(), '{name}')]]",
        )
        return self.is_visible(*locator)

    def open_task(self, name: str) -> None:
        locator = (
            By.XPATH,
            f"//*[@data-testid='board-task-card'][contains(., '{name}')]",
        )
        self.click(*locator)

    def add_comment(self, text: str) -> None:
        editor = self.wait.until(EC.visibility_of_element_located(self.EDITOR))
        editor.click()
        editor.send_keys(text)
        self.driver.execute_script("document.activeElement.blur()")

    def is_comment_visible(self, text: str) -> bool:
        locator = (
            By.XPATH,
            f"//*[@contenteditable='true' and contains(., '{text}')]",
        )
        return self.is_visible(*locator)
