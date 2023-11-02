from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def test_user_login(driver):
    """
    test_user_login just logs in a test user.
    Because this functionality is wanted in many tests, it is good to have a function that performs it.

    :param driver: a selenium web driver already at the login page of our app.
    """
    driver.find_element(By.ID, "id_username").send_keys("test_user")
    driver.find_element(By.ID, "id_password").send_keys("test_password")
    driver.find_element(By.ID, "submit_button").click()


class FirefoxManager:
    """
    FirefoxManager is a context manager for a selenium web driver for Firefox.
    It can be used to open a selenium web driver and not have to worry about closing it manually.
    It is used with a "with" expression:
    >>> with FirefoxManager() as driver: print("code body goes here")
    code body goes here
    """

    def __init__(self):
        options = Options()
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(2)
        self.driver = driver

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

class ChromeManager:
    """
    Chrome managers
    """

    def __init__(self):
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(2)
        self.driver = driver

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

driver_manager = None
