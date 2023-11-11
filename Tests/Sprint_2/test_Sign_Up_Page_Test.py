import unittest
from selenium.webdriver.common.by import By

from Tests.SeleniumSetUp import driver_manager, test_user_login


# not merged with main yet, but meant to test create account option
# need ids for  submit button
# id=id_new_account_button
# id=id_username
# id=id_password1
# id=id_password2
# id=id_submit_new_account_button

class TestNewAccount(unittest.TestCase):

    # TC 1: create new account and go to dashboard
    def test_create_account(self):
        with driver_manager() as driver:
            driver.get("http://localhost:8000/")
            driver.find_element(By.ID, "id_new_account_button").click()
            driver.find_element(By.ID, "id_username").send_keys("jefferson")
            driver.find_element(By.ID, "id_password1").send_keys("passwordg")
            driver.find_element(By.ID, "id_password2").send_keys("passwordg")
            driver.find_element(By.ID, "id_submit_new_account_button").click()
            self.assertEquals(
                "The dashboard is currently in mode My Events",
                driver.find_element(By.ID, "Current Filter Mode").text
            )

    # TC 2: create new account with weak password and get denied
    def test_weak_password(self):
        with driver_manager() as driver:
            driver.get("http://localhost:8000/")
            driver.find_element(By.ID, "id_new_account_button").click()
            driver.find_element(By.ID, "id_username").send_keys("jefferson")
            driver.find_element(By.ID, "id_password1").send_keys("1")
            driver.find_element(By.ID, "id_password2").send_keys("1")
            driver.find_element(By.ID, "id_submit_new_account_button").click()
            self.assertEquals(
                "Sign up",
                driver.find_element(By.ID, "id_submit_new_account_button").text
            )

    # TC 3: create new account with already used username and get denied
    def test_already_used_name(self):
        with driver_manager() as driver:
            driver.get("http://localhost:8000/")
            driver.find_element(By.ID, "id_new_account_button").click()
            driver.find_element(By.ID, "id_username").send_keys("jefferson")
            driver.find_element(By.ID, "id_password1").send_keys("passwordg")
            driver.find_element(By.ID, "id_password2").send_keys("passwordg")
            driver.find_element(By.ID, "id_submit_new_account_button").click()
            self.assertEquals(
                "Sign up",
                driver.find_element(By.ID, "id_submit_new_account_button").text
            )

    # TC 4: create new account with two different passwords and get denied
    def test_two_passwords(self):
        with driver_manager() as driver:
            driver.get("http://localhost:8000/")
            driver.find_element(By.ID, "id_new_account_button").click()
            driver.find_element(By.ID, "id_username").send_keys("jefferson")
            driver.find_element(By.ID, "id_password1").send_keys("passwordg")
            driver.find_element(By.ID, "id_password2").send_keys("pasbananag")
            driver.find_element(By.ID, "id_submit_new_account_button").click()
            self.assertEquals(
                "Sign up",
                driver.find_element(By.ID, "id_submit_new_account_button").text
            )

    # TC 5: create new account with a long username and get denied, currently not working reportedly (but merge still
    # please)
    def test_long_name(self):
        with driver_manager() as driver:
            driver.get("http://localhost:8000/")
            driver.find_element(By.ID, "id_new_account_button").click()
            driver.find_element(By.ID, "id_username").send_keys(15 * "atenletterwordrst")
            driver.find_element(By.ID, "id_password1").send_keys("passwordg")
            driver.find_element(By.ID, "id_password2").send_keys("passwordg")
            driver.find_element(By.ID, "id_submit_new_account_button").click()
            self.assertEquals(
                "Sign up",
                driver.find_element(By.ID, "id_submit_new_account_button").text
            )
