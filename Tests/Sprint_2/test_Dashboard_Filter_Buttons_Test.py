import unittest
from selenium.webdriver.common.by import By

from Tests.SeleniumSetUp import driver_manager, test_user_login


class TestDashboard(unittest.TestCase):
    def test_default_filter(self):
        """
        The dashboard should be in mode "My Events" when you first visit it by default.
        """
        with driver_manager() as driver:
            driver.get("http://localhost:8000/")
            test_user_login(driver)
            self.assertEquals(
                "The dashboard is currently in mode My Events",
                driver.find_element(By.ID, "Current Filter Mode").text
            )

    def test_all_to_my(self):
        """
        You should be able to click on a button to move from "All Events" to "My Events" filters on the dashboard.
        """
        with driver_manager() as driver:
            driver.get("http://localhost:8000/")
            test_user_login(driver)
            driver.find_element(By.ID, "All Events Filter").click()
            self.assertEquals(
                "The dashboard is currently in mode All Events",
                driver.find_element(By.ID, "Current Filter Mode").text
            )
            driver.find_element(By.ID, "My Events Filter").click()
            self.assertEquals(
                "The dashboard is currently in mode My Events",
                driver.find_element(By.ID, "Current Filter Mode").text
            )

    def test_all_to_inv(self):
        with driver_manager() as driver:
            driver.get("http://localhost:8000/")
            test_user_login(driver)
            driver.find_element(By.ID, "All Events Filter").click()
            self.assertEquals(
                "The dashboard is currently in mode All Events",
                driver.find_element(By.ID, "Current Filter Mode").text
            )
            driver.find_element(By.ID, "Invited Events Filter").click()
            self.assertEquals(
                "The dashboard is currently in mode Invited Events",
                driver.find_element(By.ID, "Current Filter Mode").text
            )

    def test_my_to_all(self):
        with driver_manager() as driver:
            driver.get("http://localhost:8000/")
            test_user_login(driver)
            self.assertEquals(
                "The dashboard is currently in mode My Events",
                driver.find_element(By.ID, "Current Filter Mode").text
            )
            driver.find_element(By.ID, "All Events Filter").click()
            self.assertEquals(
                "The dashboard is currently in mode All Events",
                driver.find_element(By.ID, "Current Filter Mode").text
            )

    def test_my_to_inv(self):
        with driver_manager() as driver:
            driver.get("http://localhost:8000/")
            test_user_login(driver)
            self.assertEquals(
                "The dashboard is currently in mode My Events",
                driver.find_element(By.ID, "Current Filter Mode").text
            )
            driver.find_element(By.ID, "Invited Events Filter").click()
            self.assertEquals(
                "The dashboard is currently in mode Invited Events",
                driver.find_element(By.ID, "Current Filter Mode").text
            )

    def test_inv_to_all(self):
        with driver_manager() as driver:
            driver.get("http://localhost:8000/")
            test_user_login(driver)
            driver.find_element(By.ID, "Invited Events Filter").click()
            self.assertEquals(
                "The dashboard is currently in mode Invited Events",
                driver.find_element(By.ID, "Current Filter Mode").text
            )
            driver.find_element(By.ID, "All Events Filter").click()
            self.assertEquals(
                "The dashboard is currently in mode All Events",
                driver.find_element(By.ID, "Current Filter Mode").text
            )

    def test_inv_to_my(self):
        with driver_manager() as driver:
            driver.get("http://localhost:8000/")
            test_user_login(driver)
            driver.find_element(By.ID, "Invited Events Filter").click()
            self.assertEquals(
                "The dashboard is currently in mode Invited Events",
                driver.find_element(By.ID, "Current Filter Mode").text
            )
            driver.find_element(By.ID, "My Events Filter").click()
            self.assertEquals(
                "The dashboard is currently in mode My Events",
                driver.find_element(By.ID, "Current Filter Mode").text
            )
