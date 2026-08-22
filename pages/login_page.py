from selenium.webdriver.common.by import By

from config import UI_URL
from pages.base_page import BasePage


class LoginPage(BasePage):
    LOGIN_BUTTON = (By.XPATH, "//*[contains(text(), 'Войти')]")
    EMAIL_INPUT = (By.XPATH, "//input[@placeholder='E-mail']")
    PASSWORD_INPUT = (By.XPATH, "//input[@placeholder='Пароль']")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(., 'Войти')]")
    DASHBOARD_TITLE = (By.XPATH, "//*[contains(text(), 'Проекты')]")

    def open(self) -> None:
        self.driver.get(UI_URL)

    def login(self, email: str, password: str) -> None:
        self.open()
        self.click(*self.LOGIN_BUTTON)
        self.type_text(*self.EMAIL_INPUT, email)
        self.type_text(*self.PASSWORD_INPUT, password)
        self.click(*self.SUBMIT_BUTTON)

    def is_authorized(self) -> bool:
        return self.is_visible(*self.DASHBOARD_TITLE)
