from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


def test_user_login(driver):
    driver.find_element(By.ID, "id_username").send_keys("test_user")
    driver.find_element(By.ID, "id_password").send_keys("test_password")
    driver.find_element(By.ID, "submit_button").click()


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
