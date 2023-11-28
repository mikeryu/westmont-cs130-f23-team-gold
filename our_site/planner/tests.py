from datetime import datetime

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By

from test_utils.SeleniumSetUp import driver_manager, generic_user_login
from planner.models import *


class SiteTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        # Make two users and associated profiles
        test_user0 = User.objects.create_user(
            username="test_user0",
            password="test_password",
        )
        (test_profile0 := Profile(user=test_user0)).save()
        test_user1 = User.objects.create_user(
            username="test_user1",
            password="test_password",
        )
        (test_profile1 := Profile(user=test_user1)).save()

        # Make one event owned by each user
        # Invite the first user to the event owned by the second user
        (test_event0 := Event(
            owner=test_profile0,
            name="a",
            date=datetime.now(),
            description="a",
            location="a",
        )).save()
        (test_event1 := Event(
            owner=test_profile1,
            name="b",
            date=datetime.now(),
            description="b",
            location="b",
        )).save()
        test_event1.invitees.add(test_profile0)
        test_event1.save()

    def test_edit_my_event(self) -> None:
        """

        """
        with driver_manager() as driver:
            driver.get(f"{self.live_server_url}/")
            generic_user_login(driver, "test_user0", "test_password")
            driver.find_element(By.ID, "event-title-1").click()
            self.assertEquals(
                len(driver.find_elements(By.ID, "edit-event")),
                1
            )

    def test_no_edit_not_my_event(self) -> None:
        """

        """
        with driver_manager() as driver:
            driver.get(f"{self.live_server_url}/")
            generic_user_login(driver, "test_user0", "test_password")
            driver.find_element(By.ID, "Invited Events Filter").click()
            driver.find_element(By.ID, "event-title-1").click()
            self.assertEquals(
                len(driver.find_elements(By.ID, "edit-event")),
                0
            )
