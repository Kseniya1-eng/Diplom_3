from selenium.webdriver.common.by import By


class FeedLocators:
    """Локаторы страницы «Лента заказов»."""

    FEED_HEADING = (By.XPATH, '//h1[contains(@class, "text_type_main-large") and text()="Лента заказов"]')

    # счётчики «Выполнено за всё время» и «Выполнено за сегодня»
    DONE_COUNTERS = (By.XPATH, '//p[contains(@class, "OrderFeed_number")]')

    # список заказов «В работе»
    IN_WORK_LIST = (By.XPATH, '//ul[contains(@class, "OrderFeed_orderListReady")]')
    IN_WORK_ITEMS = (By.XPATH, '//ul[contains(@class, "OrderFeed_orderListReady")]//li')
