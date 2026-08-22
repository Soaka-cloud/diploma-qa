import uuid

import allure
from selenium.webdriver.remote.webdriver import WebDriver

from pages.board_page import BoardPage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from pages.project_page import ProjectPage


def _unique_name() -> str:
    return f"Тест {uuid.uuid4()}"


@allure.feature("UI. Авторизация")
class TestLogin:
    @allure.title("Вход в систему с корректными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_successful(self, logged_in_driver: WebDriver) -> None:
        with allure.step("Проверить, что открылся дашборд"):
            assert LoginPage(logged_in_driver).is_authorized()


@allure.feature("UI. Проекты")
class TestProjects:
    @allure.title("Создание проекта")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_project(self, logged_in_driver: WebDriver) -> None:
        name = _unique_name()
        dashboard = DashboardPage(logged_in_driver)
        with allure.step("Создать проект"):
            dashboard.create_project(name)
        with allure.step("Проверить, что проект отображается в списке"):
            assert dashboard.is_project_visible(name)

    @allure.title("Редактирование названия проекта")
    @allure.severity(allure.severity_level.NORMAL)
    def test_rename_project(self, logged_in_driver: WebDriver) -> None:
        name = _unique_name()
        new_name = f"{name} (изменён)"
        dashboard = DashboardPage(logged_in_driver)
        dashboard.create_project(name)
        project = ProjectPage(logged_in_driver)
        with allure.step("Переименовать проект"):
            project.rename(new_name)
        with allure.step("Проверить новое название"):
            assert project.is_title_visible(new_name)


@allure.feature("UI. Задачи")
class TestTasks:
    @allure.title("Создание задачи на доске")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_task(self, logged_in_driver: WebDriver) -> None:
        name = _unique_name()
        dashboard = DashboardPage(logged_in_driver)
        dashboard.create_project(name)
        board = BoardPage(logged_in_driver)
        with allure.step("Создать задачу"):
            board.create_task(name)
        with allure.step("Проверить, что задача отображается на доске"):
            assert board.is_task_visible(name)

    @allure.title("Изменение статуса задачи")
    @allure.severity(allure.severity_level.NORMAL)
    def test_move_task(self, logged_in_driver: WebDriver) -> None:
        name = _unique_name()
        dashboard = DashboardPage(logged_in_driver)
        dashboard.create_project(name)
        board = BoardPage(logged_in_driver)
        board.create_task(name)
        with allure.step("Перенести задачу в другую колонку"):
            board.move_task(name)
        with allure.step("Проверить, что задача в новой колонке"):
            assert board.is_task_visible(name)

    @allure.title("Добавление комментария к задаче")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_comment(self, logged_in_driver: WebDriver) -> None:
        name = _unique_name()
        comment = f"Комментарий {uuid.uuid4()}"
        dashboard = DashboardPage(logged_in_driver)
        dashboard.create_project(name)
        board = BoardPage(logged_in_driver)
        board.create_task(name)
        with allure.step("Добавить комментарий"):
            board.add_comment(comment)
        with allure.step("Проверить, что комментарий отображается"):
            assert board.is_comment_visible(comment)
