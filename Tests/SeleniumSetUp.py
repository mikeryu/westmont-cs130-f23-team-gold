from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class FirefoxManager:
    def __init__(self):
        options = Options()
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(2)
        self.driver = driver

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


driver_manager = None
