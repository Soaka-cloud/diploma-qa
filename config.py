import os

BASE_URL = os.getenv("YOUGILE_BASE_URL", "https://yougile.com/api-v2")
UI_URL = os.getenv("YOUGILE_UI_URL", "https://yougile.com")
LOGIN = os.getenv("YOUGILE_LOGIN", "")
PASSWORD = os.getenv("YOUGILE_PASSWORD", "")
TOKEN = os.getenv("YOUGILE_KEY", "")
BROWSER = os.getenv("BROWSER", "chrome")
