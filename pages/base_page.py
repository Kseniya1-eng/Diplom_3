import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# JavaScript-эмуляция HTML5 drag&drop.
# Нативное перетаскивание Selenium (ActionChains.drag_and_drop) нестабильно
# работает в Firefox, поэтому используется JS-подход — он работает в обоих браузерах.
JS_DRAG_AND_DROP = """
function simulateDragDrop(source, target) {
    var dataTransfer = new DataTransfer();
    source.dispatchEvent(new DragEvent('dragstart', {bubbles: true, cancelable: true, dataTransfer: dataTransfer}));
    target.dispatchEvent(new DragEvent('drop', {bubbles: true, cancelable: true, dataTransfer: dataTransfer}));
    source.dispatchEvent(new DragEvent('dragend', {bubbles: true, cancelable: true, dataTransfer: dataTransfer}));
}
simulateDragDrop(arguments[0], arguments[1]);
"""


class BasePage:
    """Базовый класс Page Object с общими методами."""

    def __init__(self, driver: WebDriver, timeout: int = 20):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str):
        self.driver.get(url)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_invisible(self, locator):
        self.wait.until(EC.invisibility_of_element_located(locator))

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def wait_url(self, url: str, timeout: int | None = None) -> bool:
        try:
            WebDriverWait(self.driver, timeout or self.timeout).until(EC.url_to_be(url))
            return True
        except Exception:
            return False

    def current_url(self) -> str:
        return self.driver.current_url

    def drag_and_drop(self, source_element, target_element):
        self.driver.execute_script(JS_DRAG_AND_DROP, source_element, target_element)
        # даём React время обработать событие перетаскивания
        time.sleep(0.5)

    def click_element(self, element):
        """Кликает по элементу через JS — обходит overlay-блокировки (Firefox)."""
        self.driver.execute_script("arguments[0].click();", element)
