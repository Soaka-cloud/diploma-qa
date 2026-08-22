from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class BoardPage(BasePage):
    ADD_TASK_BUTTON = (By.XPATH, "//*[contains(text(), 'Добавить задачу')]")
    NAME_INPUT = (By.XPATH, "//input[@placeholder='Название']")
    CREATE_BUTTON = (By.XPATH, "//button[contains(., 'Создать')]")
    COMMENT_INPUT = (By.XPATH, "//textarea[@placeholder='Комментарий']")
    SEND_BUTTON = (By.XPATH, "//button[contains(., 'Отправить')]")

    def create_task(self, name: str) -> None:
        self.click(*self.ADD_TASK_BUTTON)
        self.type_text(*self.NAME_INPUT, name)
        self.click(*self.CREATE_BUTTON)

    def is_task_visible(self, name: str) -> bool:
        locator = (By.XPATH, f"//*[contains(text(), '{name}')]")
        return self.is_visible(*locator)

    def move_task(self, name: str) -> None:
        task = self.find(By.XPATH, f"//*[contains(text(), '{name}')]")
        column = self.find(By.XPATH, "//*[contains(text(), 'В работе')]")
        ActionChains(self.driver).drag_and_drop(task, column).perform()

    def add_comment(self, text: str) -> None:
        self.type_text(*self.COMMENT_INPUT, text)
        self.click(*self.SEND_BUTTON)

    def is_comment_visible(self, text: str) -> bool:
        locator = (By.XPATH, f"//*[contains(text(), '{text}')]")
        return self.is_visible(*locator)
