import re
import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from config import BROWSER, LOGIN, PASSWORD, TOKEN
from pages.login_page import LoginPage
from yougile_api import YougileApi

TEST_PROJECT_TITLE = re.compile(
    r"^(Проект|Новый|Тест-проект) \d{5}( \(изм\.\))?$"
)


def _api_token() -> str:
    if TOKEN:
        return TOKEN
    if LOGIN and PASSWORD:
        return YougileApi.get_token(LOGIN, PASSWORD)
    pytest.skip("Задайте YOUGILE_KEY или YOUGILE_LOGIN "
                "и YOUGILE_PASSWORD в .env")


def _delete_test_projects() -> None:
    """Удаляет созданные тестами проекты, чтобы не засорять пространство."""
    if not (LOGIN or TOKEN):
        return
    api = YougileApi(_api_token())
    for _ in range(4):
        try:
            projects = api.get_projects().json()["content"]
        except (ValueError, KeyError):
            return
        junk = [p for p in projects
                if TEST_PROJECT_TITLE.match(p.get("title") or "")]
        if not junk:
            return
        for project in junk:
            api.delete_project(project["id"])


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_projects() -> None:
    yield
    _delete_test_projects()


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
