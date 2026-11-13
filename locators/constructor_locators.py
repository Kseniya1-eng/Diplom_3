from selenium.webdriver.common.by import By


class ConstructorLocators:
    """Локаторы страницы конструктора (главной страницы)."""

    # ссылки в шапке
    CONSTRUCTOR_LINK = (By.XPATH, '//a[contains(@class, "AppHeader_header__link") and @href="/"]')
    FEED_LINK = (By.XPATH, '//a[contains(@class, "AppHeader_header__link") and @href="/feed"]')
    ACCOUNT_LINK = (By.XPATH, '//a[contains(@class, "AppHeader_header__link") and @href="/account"]')

    # заголовок конструктора
    CONSTRUCTOR_HEADING = (By.XPATH, '//h1[contains(@class, "text_type_main-large") and text()="Соберите бургер"]')

    # карточки ингредиентов
    INGREDIENT_CARD = (By.XPATH, '//a[contains(@class, "BurgerIngredient_ingredient")]')
    INGREDIENT_COUNTER = (By.XPATH, '//p[contains(@class, "counter_counter__num")]')

    # область конструктора, куда перетаскиваются ингредиенты
    CONSTRUCTOR_BASKET = (By.XPATH, '//section[contains(@class, "BurgerConstructor_basket")]')

    # модальное окно с деталями ингредиента
    INGREDIENT_MODAL = (By.XPATH, '//div[contains(@class, "Modal_modal") and contains(., "Детали ингредиента")]')
    INGREDIENT_DETAIL_TITLE = (By.XPATH, '//h2[contains(@class, "Modal_modal__title") and text()="Детали ингредиента"]')

    # модальное окно оформленного заказа
    ORDER_MODAL = (By.XPATH, '//div[contains(@class, "Modal_modal") and contains(., "идентификатор заказа")]')
    ORDER_NUMBER = (By.XPATH, '//h2[contains(@class, "text_type_digits-large")]')

    # кнопка «Оформить заказ»
    ORDER_BUTTON = (By.XPATH, '//button[contains(., "Оформить заказ")]')

    # крестик закрытия модального окна
    MODAL_CLOSE_BUTTON = (By.XPATH, '//button[contains(@class, "Modal_modal__close")]')
