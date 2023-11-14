import unittest
from selenium.webdriver.common.by import By

from Tests.SeleniumSetUp import driver_manager, test_user_login


class TestEventView(unittest.TestCase):
    # TC 1: create new event on create event form
    def test_create_event(self):
        with driver_manager() as driver:
            driver.get("http://localhost:8000/")
            test_user_login(driver)
            driver.find_element(By.ID, "Create New Event").click()
            driver.find_element(By.ID, "id_event_name").send_keys("Test event")
            driver.find_element(By.ID, "id_event_date").send_keys("5/2/2024 7:30")
            driver.find_element(By.ID, "id_event_description").send_keys("this is a test description")
            driver.find_element(By.ID, "id_event_location").send_keys("this is a test location")
            driver.find_element(By.ID, "create_event_btn").click()
            self.assertEquals(
                "New Event Created",
                driver.find_element(By.ID, "id_submit_new_event_button").text
            )

    # TC 2: can edit previously input event details
    def edit_new_event(self):
        with driver_manager() as driver:
            driver.get("http://localhost:8000/")
            test_user_login(driver)
            driver.find_element(By.ID, "Create New Event").click()
            driver.find_element(By.ID, "id_event_name").send_keys("Test event")
            driver.find_element(By.ID, "id_event_date").send_keys("5/2/2024 7:30")
            driver.find_element(By.ID, "id_event_description").send_keys("this is a test description")
            driver.find_element(By.ID, "id_event_location").send_keys("this is a test location")
            driver.find_element(By.ID, "create_event_btn").click()
            driver.find_element(By.ID, "id_event_name").send_keys("Test edit")
            self.assertEquals(
                "Created events can be edited",
                driver.find_element(By.ID, "id_submit_edit_events").text
            )

    # TC 3: create new event and save edited event details
    def save_edit_details(self):
        with driver_manager() as driver:
            driver.get("http://localhost:8000/")
            test_user_login(driver)
            driver.find_element(By.ID, "Create New Event").click()
            driver.find_element(By.ID, "id_event_name").send_keys("Test event")
            driver.find_element(By.ID, "id_event_date").send_keys("5/2/2024 7:30")
            driver.find_element(By.ID, "id_event_description").send_keys("this is a test description")
            driver.find_element(By.ID, "id_event_location").send_keys("this is a test location")
            driver.find_element(By.ID, "create_event_btn").click()
            driver.find_element(By.ID, "id_event_name").send_keys("Test edit")
            driver.find_element(By.ID, "save_changes_btn").click()
            self.assertEquals(
                "The editted changes have been saved",
                driver.find_element(By.ID, "id_submit_save_changes").text
            )

    # TC 4: create new event and filter by sort buttons
    def new_event_sorted(self):
        with driver_manager() as driver:
            driver.get("http://localhost:8000/")
            test_user_login(driver)
            driver.find_element(By.ID, "Create New Event").click()
            driver.find_element(By.ID, "id_event_name").send_keys("Test event")
            driver.find_element(By.ID, "id_event_date").send_keys("5/2/2024 7:30")
            driver.find_element(By.ID, "id_event_description").send_keys("this is a test description")
            driver.find_element(By.ID, "id_event_location").send_keys("this is a test location")
            driver.find_element(By.ID, "create_event_btn").click()
            driver.find_element(By.ID, "return_to_dashboard_btn").click()
            driver.find_element(By.ID, "all_events_filter").click()
            self.assertEquals(
                "The new event is sorted by All Events",
                driver.find_element(By.ID, "id_current_filter").text
            )
            driver.find_element(By.ID, "my_events_filter").click()
            self.assertEquals(
                "The new event is sorted by My Events",
                driver.find_element(By.ID, "id_current_filter").text
            )
            driver.find_element(By.ID, "invited_events_filter").click()
            self.assertEquals(
                "The new event is sorted by Invited Events",
                driver.find_element(By.ID, "id_current_filter").text
            )
