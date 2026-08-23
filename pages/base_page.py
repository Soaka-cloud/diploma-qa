from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)

    def find(self, by: str, locator: str) -> WebElement:
        return self.wait.until(EC.presence_of_element_located((by, locator)))

    def click(self, by: str, locator: str) -> None:
        self.wait.until(EC.element_to_be_clickable((by, locator))).click()

    def type_text(self, by: str, locator: str, text: str) -> None:
        self.find(by, locator).send_keys(text)

    def press_enter(self, by: str, locator: str) -> None:
        self.find(by, locator).send_keys(Keys.ENTER)

    def is_visible(self, by, locator) -> bool:
        condition = EC.visibility_of_element_located((by, locator))
        return bool(self.wait.until(condition))

    def is_visible_short(self, by, locator, timeout: int = 10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, locator)))
            return True
        except TimeoutException:
            return False
