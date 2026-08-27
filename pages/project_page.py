from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage


class ProjectPage(BasePage):
    RENAME_ITEM = (By.XPATH, "//*[contains(text(), 'Переименовать')]")
    NAME_INPUT = (
        By.XPATH, "//input[@placeholder='Введите название проекта…']",
    )

    def rename(self, name: str, new_title: str) -> None:
        card = (
            By.XPATH,
            f"//*[@data-testid='project-card'][contains(., '{name}')]",
        )
        if not self.find_in_scrollable_list(card, timeout=90):
            raise TimeoutException(
                f"Карточка проекта «{name}» не найдена в списке проектов"
            )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            self.driver.find_element(*card),
        )
        menu_button = (
            By.XPATH,
            f"//*[@data-testid='project-card'][contains(., '{name}')]"
            f"//*[@data-testid='project-card-menu-button']",
        )
        self.click_js(*menu_button)
        self.click(*self.RENAME_ITEM)
        field = self.find(*self.NAME_INPUT)
        field.send_keys(Keys.CONTROL, "a")
        field.send_keys(new_title)
        self.press_enter(*self.NAME_INPUT)

    def is_title_visible(self, title: str) -> bool:
        locator = (
            By.XPATH,
            f"//*[@data-testid='project-card'][contains(., '{title}')]",
        )
        return self.wait_for_presence(*locator, timeout=60)
