from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProjectPage(BasePage):
    TITLE_LABEL = (By.XPATH, "//*[contains(@class, 'title')]")
    NAME_INPUT = (By.XPATH, "//input[@placeholder='Название']")
    SAVE_BUTTON = (By.XPATH, "//button[contains(., 'Сохранить')]")

    def rename(self, new_title: str) -> None:
        self.click(*self.TITLE_LABEL)
        self.type_text(*self.NAME_INPUT, new_title)
        self.click(*self.SAVE_BUTTON)

    def is_title_visible(self, title: str) -> bool:
        locator = (By.XPATH, f"//*[contains(text(), '{title}')]")
        return self.is_visible(*locator)
