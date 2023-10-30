import unittest
from selenium.webdriver.common.by import By

from Tests.SeleniumSetUp import driver_manager, test_user_login


class TestDashboard(unittest.TestCase):
    def test_default_filter(self):
        with driver_manager() as driver:
            driver.get("http://localhost:8000/")
            test_user_login(driver)

    def test_all_to_my(self):
        self.assertEquals(True, False)

    def test_all_to_inv(self):
        self.assertEquals(True, False)

    def test_my_to_all(self):
        self.assertEquals(True, False)

    def test_my_to_inv(self):
        self.assertEquals(True, False)

    def test_inv_to_all(self):
        self.assertEquals(True, False)

    def test_inv_to_my(self):
        self.assertEquals(True, False)
