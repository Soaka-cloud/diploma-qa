from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class DashboardPage(BasePage):
    CREATE_BUTTON = (By.XPATH, "//*[@data-testid='add-project-button']")
    MENU_PROJECT = (
        By.XPATH, "//*[@data-testid='menu-item-add-default-project']",
    )
    NAME_INPUT = (
        By.XPATH, "//input[@placeholder='Введите название проекта…']",
    )
    SUBMIT_BUTTON = (
        By.XPATH, "//div[contains(text(), 'Добавить проект с задачами')]",
    )

    def create_project(self, name: str) -> None:
        self.click(*self.CREATE_BUTTON)
        self.click(*self.MENU_PROJECT)
        self.type_text(*self.NAME_INPUT, name)
        self.click(*self.SUBMIT_BUTTON)
        panel = "//*[@data-testid='project-name-upper-panel']"
        self.is_visible(By.XPATH, panel)

    def is_project_visible(self, name: str) -> bool:
        locator = (
            By.XPATH,
            f"//*[@data-testid='project-name-upper-panel']"
            f"[contains(., '{name}')]",
        )
        return self.is_visible(*locator)
