import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from config import BROWSER, LOGIN, PASSWORD, TOKEN
from pages.login_page import LoginPage
from yougile_api import YougileApi


def _api_token() -> str:
    if TOKEN:
        return TOKEN
    if LOGIN and PASSWORD:
        return YougileApi.get_token(LOGIN, PASSWORD)
    pytest.skip("Задайте YOUGILE_KEY или YOUGILE_LOGIN "
                "и YOUGILE_PASSWORD в .env")


@pytest.fixture
def api() -> YougileApi:
    return YougileApi(_api_token())


def _make_driver() -> WebDriver:
    browser = BROWSER.lower()
    if browser == "firefox":
        return webdriver.Firefox()
    if browser == "edge":
        return webdriver.Edge()
    return webdriver.Chrome()


@pytest.fixture
def driver() -> WebDriver:
    driver = _make_driver()
    yield driver
    driver.quit()


@pytest.fixture
def logged_in_driver(driver: WebDriver) -> WebDriver:
    if not (LOGIN and PASSWORD):
        pytest.skip("Задайте YOUGILE_LOGIN и YOUGILE_PASSWORD для UI-тестов")
    LoginPage(driver).login(LOGIN, PASSWORD)
    return driver
