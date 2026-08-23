import requests

from config import BASE_URL


class YougileApi:
    BASE_URL = BASE_URL

    def __init__(self, token: str) -> None:
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"}

    @staticmethod
    def get_token(login: str, password: str) -> str:
        resp = requests.post(
            f"{YougileApi.BASE_URL}/auth/keys/get",
            json={"login": login, "password": password},
        )
        resp.raise_for_status()
        return resp.json()[0]["key"]

    def get_projects(self) -> requests.Response:
        return requests.get(f"{self.BASE_URL}/projects", headers=self.headers)

    def create_project(self, title: str) -> requests.Response:
        return requests.post(
            f"{self.BASE_URL}/projects",
            json={"title": title},
            headers=self.headers,
        )

    def get_project(self, project_id: str) -> requests.Response:
        return requests.get(
            f"{self.BASE_URL}/projects/{project_id}",
            headers=self.headers,
        )

    def update_project(self, project_id: str, title: str) -> requests.Response:
        return requests.put(
            f"{self.BASE_URL}/projects/{project_id}",
            json={"title": title},
            headers=self.headers,
        )

    def get_boards(self) -> requests.Response:
        return requests.get(f"{self.BASE_URL}/boards", headers=self.headers)

    def create_column(self, title: str, board_id: str) -> requests.Response:
        return requests.post(
            f"{self.BASE_URL}/columns",
            json={"title": title, "boardId": board_id},
            headers=self.headers,
        )
