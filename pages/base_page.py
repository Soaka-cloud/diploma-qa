import time

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

    def click_js(self, by: str, locator: str) -> None:
        self.find(by, locator)
        self.driver.execute_script(
            "arguments[0].click();",
            self.driver.find_element(by, locator),
        )

    def wait_for_presence(self, by: str, locator: str,
                          timeout: int = 60, poll: float = 2.0) -> bool:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.driver.find_elements(by, locator):
                return True
            time.sleep(poll)
        return False

    def find_in_scrollable_list(self, locator: tuple,
                                timeout: int = 90) -> bool:
        """Ищет элемент в виртуализированном списке, прокручивая его."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.driver.find_elements(*locator):
                return True
            self.driver.execute_script(
                "var list = document.querySelector("
                "'[data-testid=\"projects-list\"]');"
                "if (list) { list.scrollTop += 700; }"
                "else { window.scrollBy(0, 700); }"
            )
            time.sleep(1.2)
            at_bottom = self.driver.execute_script(
                "var list = document.querySelector("
                "'[data-testid=\"projects-list\"]');"
                "if (list) {"
                "  return list.scrollTop + list.clientHeight"
                "         >= list.scrollHeight;"
                "}"
                "return window.innerHeight + window.scrollY"
                "       >= document.body.scrollHeight;"
            )
            if at_bottom:
                self.driver.refresh()
                time.sleep(3)
        return False

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
