import uuid

import allure
import pytest
import requests

from config import BASE_URL, LOGIN, PASSWORD
from yougile_api import YougileApi


def _unique_name() -> str:
    return f"Проект {uuid.uuid4()}"


@allure.feature("API. Авторизация")
class TestAuth:
    @allure.title("Получение токена с корректными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_auth_get_token(self, api: YougileApi) -> None:
        if not (LOGIN and PASSWORD):
            pytest.skip("Задайте YOUGILE_LOGIN и YOUGILE_PASSWORD в .env")
        with allure.step("Запросить токен через auth/keys/get"):
            token = YougileApi.get_token(LOGIN, PASSWORD)
        with allure.step("Проверить, что токен получен"):
            assert token


@allure.feature("API. Проекты")
class TestProjects:
    @allure.title("Получение списка проектов с токеном")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_projects_with_token(self, api: YougileApi) -> None:
        with allure.step("Выполнить GET /projects"):
            resp = api.get_projects()
        with allure.step("Проверить статус-код 200"):
            assert resp.status_code == 200
        with allure.step("Проверить, что ответ содержит список проектов"):
            body = resp.json()
            assert "content" in body
            assert isinstance(body["content"], list)

    @allure.title("Создание проекта")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_project(self, api: YougileApi) -> None:
        title = _unique_name()
        with allure.step("Выполнить POST /projects"):
            resp = api.create_project(title)
        with allure.step("Проверить статус-код 201"):
            assert resp.status_code == 201
        project_id = resp.json()["id"]
        with allure.step("Получить созданный проект и сверить название"):
            created = api.get_project(project_id).json()
            assert created["title"] == title

    @allure.title("Получение проекта по ID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_project_by_id(self, api: YougileApi) -> None:
        project_id = api.create_project(_unique_name()).json()["id"]
        with allure.step("Выполнить GET /projects/{id}"):
            resp = api.get_project(project_id)
        with allure.step("Проверить статус-код 200 и соответствие id"):
            assert resp.status_code == 200
            assert resp.json()["id"] == project_id

    @allure.title("Обновление проекта")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_project(self, api: YougileApi) -> None:
        project_id = api.create_project(_unique_name()).json()["id"]
        new_title = f"Новый {uuid.uuid4()}"
        with allure.step("Выполнить PUT /projects/{id}"):
            resp = api.update_project(project_id, new_title)
        with allure.step("Проверить статус-код 200 и новое название"):
            assert resp.status_code == 200
            assert api.get_project(project_id).json()["title"] == new_title

    @allure.title("Создание проекта без названия")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_project_without_title(self, api: YougileApi) -> None:
        with allure.step("Выполнить POST /projects с пустым телом"):
            resp = requests.post(
                f"{BASE_URL}/projects",
                json={},
                headers=api.headers,
            )
        with allure.step("Проверить статус-код 400"):
            assert resp.status_code == 400

    @allure.title("Получение несуществующего проекта")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_nonexistent_project(self, api: YougileApi) -> None:
        with allure.step("Выполнить GET /projects/{несуществующий id}"):
            resp = api.get_project(str(uuid.uuid4()))
        with allure.step("Проверить статус-код 404"):
            assert resp.status_code == 404

    @allure.title("Получение списка проектов без токена")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_projects_without_token(self) -> None:
        with allure.step("Выполнить GET /projects без заголовка авторизации"):
            resp = requests.get(f"{BASE_URL}/projects")
        with allure.step("Проверить статус-код 401"):
            assert resp.status_code == 401


@allure.feature("API. Валидация авторизации")
class TestAuthValidation:
    @allure.title("Авторизация без пароля")
    @allure.severity(allure.severity_level.NORMAL)
    def test_auth_without_password(self) -> None:
        with allure.step("Выполнить POST /auth/keys/get без пароля"):
            resp = requests.post(
                f"{BASE_URL}/auth/keys/get",
                json={"login": "test@example.com"},
            )
        with allure.step("Проверить статус-код 400"):
            assert resp.status_code == 400
