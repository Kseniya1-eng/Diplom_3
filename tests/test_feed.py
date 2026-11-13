import allure

from data.urls import FEED_URL
from pages.constructor_page import ConstructorPage
from pages.feed_page import FeedPage
from pages.login_page import LoginPage


@allure.story('Лента заказов: счётчики и заказы в работе')
class TestFeed:

    @allure.title('При создании заказа счётчик «Выполнено за всё время» увеличивается')
    def test_all_time_counter_increases_after_order(self, driver, registered_user):
        constructor_page = ConstructorPage(driver)
        feed_page = FeedPage(driver)
        login_page = LoginPage(driver)

        # логинимся под созданным пользователем
        login_page.open_login()
        login_page.login(registered_user['email'], registered_user['password'])

        # считываем значение счётчика «Выполнено за всё время» до заказа
        feed_page.open_feed()
        counter_before = feed_page.get_done_all_time_counter()

        # собираем и оформляем заказ
        constructor_page.open_constructor()
        constructor_page.add_ingredient_to_order(0)   # булка
        constructor_page.add_ingredient_to_order(4)   # начинка
        constructor_page.place_order()
        constructor_page.wait_order_modal()
        constructor_page.close_modal()

        # считываем значение счётчика после заказа
        feed_page.open_feed()
        counter_after = feed_page.get_done_all_time_counter()

        assert counter_after > counter_before

    @allure.title('При создании заказа счётчик «Выполнено за сегодня» увеличивается')
    def test_today_counter_increases_after_order(self, driver, registered_user):
        constructor_page = ConstructorPage(driver)
        feed_page = FeedPage(driver)
        login_page = LoginPage(driver)

        login_page.open_login()
        login_page.login(registered_user['email'], registered_user['password'])

        feed_page.open_feed()
        counter_before = feed_page.get_done_today_counter()

        constructor_page.open_constructor()
        constructor_page.add_ingredient_to_order(0)
        constructor_page.add_ingredient_to_order(4)
        constructor_page.place_order()
        constructor_page.wait_order_modal()
        constructor_page.close_modal()

        feed_page.open_feed()
        counter_after = feed_page.get_done_today_counter()

        assert counter_after > counter_before

    @allure.title('После оформления заказа его номер появляется в разделе «В работе»')
    def test_order_number_appears_in_work_section(self, driver, registered_user):
        constructor_page = ConstructorPage(driver)
        feed_page = FeedPage(driver)
        login_page = LoginPage(driver)

        login_page.open_login()
        login_page.login(registered_user['email'], registered_user['password'])

        constructor_page.open_constructor()
        constructor_page.add_ingredient_to_order(0)
        constructor_page.add_ingredient_to_order(4)
        constructor_page.place_order()
        constructor_page.wait_order_modal()
        order_number = int(constructor_page.get_order_number())
        constructor_page.close_modal()

        # проверяем, что номер заказа есть в разделе «В работе» ленты заказов
        feed_page.open_feed()
        assert feed_page.is_order_in_work(order_number)
