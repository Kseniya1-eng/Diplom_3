import allure

from data.urls import CONSTRUCTOR_URL, LOGIN_URL
from locators.login_locators import LoginLocators
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object страницы входа."""

    def open_login(self):
        with allure.step('Открыть страницу входа'):
            self.open(LOGIN_URL)

    def fill_login_form(self, email: str, password: str):
        with allure.step(f'Заполнить форму входа (email: {email})'):
            self.find_element(LoginLocators.EMAIL_FIELD).send_keys(email)
            self.find_element(LoginLocators.PASSWORD_FIELD).send_keys(password)

    def click_login_button(self):
        with allure.step('Кликнуть на кнопку «Войти»'):
            self.click(LoginLocators.LOGIN_BUTTON)

    def login(self, email: str, password: str):
        with allure.step(f'Выполнить вход под пользователем {email}'):
            self.fill_login_form(email, password)
            self.click_login_button()
            # ждём редиректа на главную — значит вход выполнен успешно
            assert self.wait_url(CONSTRUCTOR_URL), 'Вход не выполнен: не произошёл переход на главную страницу'
