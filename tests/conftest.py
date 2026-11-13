from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import pytest

from helpers import create_user_via_api, delete_user_via_api


def pytest_addoption(parser):
    parser.addoption(
        '--browser',
        action='store',
        default='chrome',
        help='Браузер для запуска тестов: chrome или firefox',
    )


@pytest.fixture
def driver(request):
    """Фикстура, создающая WebDriver для выбранного браузера."""
    browser = request.config.getoption('--browser').lower()

    if browser == 'firefox':
        options = FirefoxOptions()
        options.add_argument('--width=1400')
        options.add_argument('--height=1000')
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options,
        )
    else:
        options = Options()
        options.add_argument('--window-size=1400,1000')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
        )

    yield driver
    driver.quit()


@pytest.fixture
def registered_user():
    """Создаёт пользователя через API и удаляет его после теста."""
    user = create_user_via_api()
    yield user
    delete_user_via_api(user['token'])
