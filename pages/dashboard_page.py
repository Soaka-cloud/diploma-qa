from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class DashboardPage(BasePage):
    CREATE_BUTTON = (By.XPATH, "//*[contains(text(), 'Создать проект')]")
    NAME_INPUT = (By.XPATH, "//input[@placeholder='Название']")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(., 'Создать')]")

    def create_project(self, name: str) -> None:
        self.click(*self.CREATE_BUTTON)
        self.type_text(*self.NAME_INPUT, name)
        self.click(*self.SUBMIT_BUTTON)

    def is_project_visible(self, name: str) -> bool:
        locator = (By.XPATH, f"//*[contains(text(), '{name}')]")
        return self.is_visible(*locator)
