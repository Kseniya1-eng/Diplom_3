"""Отладочный скрипт: воспроизводит feed-сценарий и пишет шаги в файл debug_feed.txt."""
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from helpers import create_user_via_api, delete_user_via_api
from pages.constructor_page import ConstructorPage
from pages.feed_page import FeedPage
from pages.login_page import LoginPage

REPORT = 'debug_feed.txt'
lines = []

def log(*a):
    lines.append(' '.join(str(x) for x in a))
    with open(REPORT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def make_driver():
    opts = Options()
    opts.add_argument('--window-size=1400,1000')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--no-sandbox')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)


try:
    user = create_user_via_api()
    log('1. user created via api, email=', user['email'])
    driver = make_driver()
    log('2. driver created')
    try:
        login = LoginPage(driver)
        login.open_login()
        log('3. login page opened, url =', login.current_url())
        login.fill_login_form(user['email'], user['password'])
        log('4. login form filled')
        login.click_login_button()
        log('5. login button clicked')
        driver.implicitly_wait(8)
        log('6. url after login =', login.current_url())

        feed = FeedPage(driver)
        feed.open_feed()
        log('7. feed opened, url =', feed.current_url())
        c = feed.get_done_all_time_counter()
        log('8. all-time counter =', c)

        con = ConstructorPage(driver)
        con.open_constructor()
        log('9. constructor opened')
        con.add_ingredient_to_order(0)
        log('10. bun dragged')
        con.add_ingredient_to_order(4)
        log('11. filling dragged')
        driver.implicitly_wait(5)
        con.place_order()
        log('12. order button clicked')
        con.wait_order_modal()
        num = con.get_order_number()
        log('13. order number =', num)
        con.close_modal()
        log('14. modal closed')

        feed.open_feed()
        log('15. feed reopened, url =', feed.current_url())
        c2 = feed.get_done_all_time_counter()
        log('16. all-time counter after =', c2, '| increased =', c2 > c)
        in_work = feed.get_in_work_order_numbers()
        log('17. in work list =', in_work)
        log('18. order in work =', str(int(num)).zfill(5) in in_work)
    finally:
        driver.quit()
        log('19. driver quit')
        delete_user_via_api(user['token'])
        log('20. user deleted')
except Exception as e:
    log('EXCEPTION:', type(e).__name__, str(e))
    log(traceback.format_exc())

print('done')
