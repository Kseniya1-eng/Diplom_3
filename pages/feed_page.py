import time

import allure

from data.urls import FEED_URL
from locators.feed_locators import FeedLocators
from pages.base_page import BasePage


class FeedPage(BasePage):
    """Page Object страницы «Лента заказов»."""

    def open_feed(self):
        with allure.step('Открыть ленту заказов'):
            self.open(FEED_URL)

    def is_feed_heading_visible(self) -> bool:
        with allure.step('Проверить видимость заголовка «Лента заказов»'):
            try:
                self.wait_visible(FeedLocators.FEED_HEADING)
                return True
            except Exception:
                return False

    def _get_done_counters(self) -> list:
        self.wait_visible(FeedLocators.DONE_COUNTERS)
        elements = self.driver.find_elements(*FeedLocators.DONE_COUNTERS)
        return elements

    def get_done_all_time_counter(self) -> int:
        with allure.step('Получить счётчик «Выполнено за всё время»'):
            return int(self._get_done_counters()[0].text)

    def get_done_today_counter(self) -> int:
        with allure.step('Получить счётчик «Выполнено за сегодня»'):
            return int(self._get_done_counters()[1].text)

    def get_in_work_order_numbers(self) -> list:
        with allure.step('Получить номера заказов в разделе «В работе»'):
            self.wait_visible(FeedLocators.IN_WORK_LIST)
            items = self.driver.find_elements(*FeedLocators.IN_WORK_ITEMS)
            return [item.text.strip() for item in items if item.text.strip()]

    def is_order_in_work(self, order_number: int) -> bool:
        with allure.step(f'Проверить наличие заказа {order_number} в разделе «В работе»'):
            normalized = str(order_number).zfill(5)
            # лента обновляется через WebSocket, поэтому опрашиваем список несколько раз
            for _ in range(10):
                numbers = self.get_in_work_order_numbers()
                if normalized in numbers:
                    return True
                time.sleep(1)
            return False
