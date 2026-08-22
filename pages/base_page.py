from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def find(self, by: str, locator: str) -> WebElement:
        return self.wait.until(EC.presence_of_element_located((by, locator)))

    def click(self, by: str, locator: str) -> None:
        self.wait.until(EC.element_to_be_clickable((by, locator))).click()

    def type_text(self, by: str, locator: str, text: str) -> None:
        self.find(by, locator).send_keys(text)

    def is_visible(self, by: str, locator: str) -> bool:
        condition = EC.visibility_of_element_located((by, locator))
        return bool(self.wait.until(condition))
