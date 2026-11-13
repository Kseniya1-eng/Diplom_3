from selenium.webdriver.common.by import By


class LoginLocators:
    """Локаторы страницы входа."""

    EMAIL_FIELD = (By.XPATH, '//input[@type="text" or @type="email"]')
    PASSWORD_FIELD = (By.XPATH, '//input[@type="password"]')
    LOGIN_BUTTON = (By.XPATH, '//button[contains(., "Войти")]')
