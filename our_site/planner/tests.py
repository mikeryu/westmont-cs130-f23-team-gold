from datetime import datetime
from time import sleep

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

    def test_something(self) -> None:
        with driver_manager() as driver:
            driver.get(f"{self.live_server_url}/")
            generic_user_login(driver, "test_user0", "test_password")
            self.assertEquals(
                "The dashboard is currently in mode My Events",
                driver.find_element(By.ID, "Current Filter Mode").text
            )
