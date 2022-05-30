# Current autotest using UI to check that Google calculations are correct
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pytest


class Helper:
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.maximize_window()
        self.browser.implicitly_wait(10)
        self.url = 'http://www.google.com/'

    # Method opens needed URL-address in browser window
    def open_start_page(self):
        self.browser.get(self.url)

    # Method closes browser-window
    def quit(self):
        self.browser.quit()

    # Additional method for checking that needed element is on page
    def element_is_present(self, method, locator):
        self.browser.implicitly_wait(2)
        try:
            self.browser.find_element(method, locator)
            return True
        except NoSuchElementException:
            return False
        finally:
            self.browser.implicitly_wait(3)

    # Method realises search google-calculator via Google-search
    def search_calculator(self):
        if self.element_is_present(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input'):
            self.browser.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').click()
            self.browser.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys('Калькулятор')
            self.browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[2]/div[2]/div[5]/center/input[1]').click()

    # Method realises users actions for entering expression and getting result
    def calculate_expression(self):
        if self.element_is_present(By.XPATH, '//*[@id="rso"]/div[1]/div/div/div[1]/div/div/div[1]/div[2]/div[2]/div/div'):
            self.browser.find_element(By.XPATH,
                                 '//*[@id="rso"]/div[1]/div/div/div[1]/div/div/div[3]/div/table[2]/tbody/tr[4]/td[1]/div/div').click()
            self.browser.find_element(By.XPATH,
                                 '//*[@id="rso"]/div[1]/div/div/div[1]/div/div/div[3]/div/table[2]/tbody/tr[3]/td[4]/div/div').click()
            self.browser.find_element(By.XPATH,
                                 '//*[@id="rso"]/div[1]/div/div/div[1]/div/div/div[3]/div/table[2]/tbody/tr[4]/td[2]/div/div').click()
            self.browser.find_element(By.XPATH,
                                 '//*[@id="rso"]/div[1]/div/div/div[1]/div/div/div[3]/div/table[2]/tbody/tr[4]/td[4]/div/div').click()
            self.browser.find_element(By.XPATH,
                                 '//*[@id="rso"]/div[1]/div/div/div[1]/div/div/div[3]/div/table[2]/tbody/tr[4]/td[3]/div/div').click()
            self.browser.find_element(By.XPATH,
                                 '//*[@id="rso"]/div[1]/div/div/div[1]/div/div/div[3]/div/table[2]/tbody/tr[5]/td[4]/div/div').click()
            self.browser.find_element(By.XPATH,
                                 '//*[@id="rso"]/div[1]/div/div/div[1]/div/div/div[3]/div/table[2]/tbody/tr[4]/td[1]/div/div').click()
            self.browser.find_element(By.XPATH,
                                 '//*[@id="rso"]/div[1]/div/div/div[1]/div/div/div[3]/div/table[2]/tbody/tr[5]/td[3]/div/div').click()

    # Additional method for getting result of calculations in string form
    def calculation_result(self):
        if self.element_is_present(By.XPATH, '//*[@id="cwos"]'):
            return self.browser.find_element(By.XPATH, '//*[@id="cwos"]').text

    # Additional method for getting entered expression in memory string
    def memory_string(self):
        if self.element_is_present(By.XPATH, '//*[@id="cwos"]'):
            return self.browser.find_element(By.XPATH, '//*[@id="rso"]/div[1]/div/div/div[1]/div/div/div[1]/div[2]/div[1]/div/span').text



fixture = None
@pytest.fixture()
def app():
    global fixture
    if fixture is None:
        fixture = Helper()
        fixture.open_start_page()

    return fixture


@pytest.fixture(autouse=True, scope='session')
def stop(request):
    def teardown():
        fixture.quit()
    request.addfinalizer(teardown)


def test_calculation_and_result(app):
    app.search_calculator()
    app.calculate_expression()

    assert app.memory_string() == '1 × 2 - 3 + 1 =', \
        f"Выражение в строке памяти не совпадает с введённым пользователем!!!"

    assert app.calculation_result() == '0', \
        f"Значение в строке результата не верно!!!"