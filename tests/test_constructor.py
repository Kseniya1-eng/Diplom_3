import allure

from data.urls import CONSTRUCTOR_URL, FEED_URL
from pages.constructor_page import ConstructorPage


@allure.story('Основная функциональность конструктора')
class TestConstructor:

    @allure.title('Переход по клику на «Конструктор»')
    def test_click_constructor_navigates_to_constructor(self, driver):
        constructor_page = ConstructorPage(driver)
        # открываем ленту заказов, затем кликаем на «Конструктор»
        constructor_page.open_constructor()
        constructor_page.click_feed_link()
        assert constructor_page.current_url() == FEED_URL

        constructor_page.click_constructor_link()

        assert constructor_page.current_url() == CONSTRUCTOR_URL
        assert constructor_page.is_constructor_heading_visible()

    @allure.title('Переход по клику на раздел «Лента заказов»')
    def test_click_feed_navigates_to_feed(self, driver):
        constructor_page = ConstructorPage(driver)
        constructor_page.open_constructor()

        constructor_page.click_feed_link()

        assert constructor_page.current_url() == FEED_URL

    @allure.title('Клик на ингредиент открывает окно с деталями')
    def test_click_ingredient_opens_details_modal(self, driver):
        constructor_page = ConstructorPage(driver)
        constructor_page.open_constructor()

        constructor_page.click_ingredient(0)

        assert constructor_page.is_ingredient_detail_modal_present()

    @allure.title('Модальное окно с деталями закрывается кликом по крестику')
    def test_close_ingredient_modal_by_cross(self, driver):
        constructor_page = ConstructorPage(driver)
        constructor_page.open_constructor()

        constructor_page.click_ingredient(0)
        assert constructor_page.is_ingredient_detail_modal_present()

        constructor_page.close_modal()

        assert constructor_page.is_modal_closed()

    @allure.title('При добавлении ингредиента в заказ счётчик увеличивается')
    def test_adding_ingredient_increases_counter(self, driver):
        constructor_page = ConstructorPage(driver)
        constructor_page.open_constructor()

        # выбираем соус (не булку), чтобы счётчик увеличился на 1
        sauce_index = 2
        counter_before = int(constructor_page.get_ingredient_counter(sauce_index))

        constructor_page.add_ingredient_to_order(sauce_index)

        counter_after = int(constructor_page.get_ingredient_counter(sauce_index))
        assert counter_after == counter_before + 1
