import allure

from data.urls import CONSTRUCTOR_URL
from locators.constructor_locators import ConstructorLocators
from pages.base_page import BasePage


class ConstructorPage(BasePage):
    """Page Object главной страницы / конструктора бургера."""

    def open_constructor(self):
        with allure.step('Открыть конструктор'):
            self.open(CONSTRUCTOR_URL)

    def click_constructor_link(self):
        with allure.step('Кликнуть на «Конструктор» в шапке'):
            self.click(ConstructorLocators.CONSTRUCTOR_LINK)

    def click_feed_link(self):
        with allure.step('Кликнуть на «Лента заказов» в шапке'):
            self.click(ConstructorLocators.FEED_LINK)

    def is_constructor_heading_visible(self) -> bool:
        with allure.step('Проверить видимость заголовка «Соберите бургер»'):
            try:
                self.wait_visible(ConstructorLocators.CONSTRUCTOR_HEADING)
                return True
            except Exception:
                return False

    def get_ingredient_cards(self):
        with allure.step('Получить карточки ингредиентов'):
            return self.find_elements(ConstructorLocators.INGREDIENT_CARD)

    def get_ingredient_counter(self, index: int) -> str:
        with allure.step(f'Получить значение счётчика ингредиента №{index}'):
            return self.find_elements(ConstructorLocators.INGREDIENT_COUNTER)[index].text

    def click_ingredient(self, index: int):
        with allure.step(f'Кликнуть на ингредиент №{index}'):
            cards = self.get_ingredient_cards()
            cards[index].click()

    def wait_ingredient_detail_modal(self):
        with allure.step('Дождаться появления окна с деталями ингредиента'):
            return self.wait_visible(ConstructorLocators.INGREDIENT_DETAIL_TITLE)

    def is_ingredient_detail_modal_present(self) -> bool:
        with allure.step('Проверить видимость окна с деталями ингредиента'):
            try:
                self.wait_visible(ConstructorLocators.INGREDIENT_MODAL)
                return True
            except Exception:
                return False

    def close_modal(self):
        with allure.step('Закрыть модальное окно кликом по крестику'):
            # JS-клик обходит overlay-блокировки (Firefox)
            element = self.wait_visible(ConstructorLocators.MODAL_CLOSE_BUTTON)
            self.click_element(element)

    def is_modal_closed(self) -> bool:
        with allure.step('Проверить, что модальное окно закрыто'):
            try:
                self.wait_invisible(ConstructorLocators.INGREDIENT_MODAL)
                return True
            except Exception:
                return False

    def add_ingredient_to_order(self, index: int):
        with allure.step(f'Добавить ингредиент №{index} в заказ'):
            cards = self.get_ingredient_cards()
            basket = self.find_element(ConstructorLocators.CONSTRUCTOR_BASKET)
            self.drag_and_drop(cards[index], basket)

    def place_order(self):
        with allure.step('Оформить заказ'):
            self.click(ConstructorLocators.ORDER_BUTTON)

    def wait_order_modal(self):
        with allure.step('Дождаться окна с номером заказа'):
            return self.wait_visible(ConstructorLocators.ORDER_NUMBER)

    def get_order_number(self) -> str:
        with allure.step('Получить номер заказа из модального окна'):
            return self.wait_visible(ConstructorLocators.ORDER_NUMBER).text.strip()
