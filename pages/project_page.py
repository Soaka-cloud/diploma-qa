from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage


class ProjectPage(BasePage):
    RENAME_ITEM = (By.XPATH, "//*[contains(text(), 'Переименовать')]")
    NAME_INPUT = (
        By.XPATH, "//input[@placeholder='Введите название проекта…']",
    )

    def rename(self, name: str, new_title: str) -> None:
        menu_button = (
            By.XPATH,
            f"//*[@data-testid='project-card'][contains(., '{name}')]"
            f"//*[@data-testid='project-card-menu-button']",
        )
        self.click(*menu_button)
        self.click(*self.RENAME_ITEM)
        field = self.find(*self.NAME_INPUT)
        field.send_keys(Keys.CONTROL, "a")
        field.send_keys(new_title)
        self.press_enter(*self.NAME_INPUT)

    def is_title_visible(self, title: str) -> bool:
        locator = (
            By.XPATH,
            f"//*[@data-testid='project-card'][contains(., '{title}')]",
        )
        return self.is_visible(*locator)
