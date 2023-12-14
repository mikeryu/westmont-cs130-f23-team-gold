from datetime import datetime
import time

import selenium
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By

from test_utils.SeleniumSetUp import driver_manager, generic_user_login
from planner.models import *


# class DashboardTest(StaticLiveServerTestCase):
#     def setUp(self) -> None:
#         # Make two users and associated profiles
#         test_user0 = User.objects.create_user(
#             username="test_user0",
#             password="test_password",
#         )
#         (test_profile0 := Profile(user=test_user0)).save()
#         test_user1 = User.objects.create_user(
#             username="test_user1",
#             password="test_password",
#         )
#         (test_profile1 := Profile(user=test_user1)).save()
# #
#         # Make one event owned by each user
#         # Invite the first user to the event owned by the second user
#         (test_event0 := Event(
#             owner=test_profile0,
#             name="a",
#             date=datetime.now(),
#             description="a",
#             location="a",
#         )).save()
#         (test_event1 := Event(
#             owner=test_profile1,
#             name="b",
#             date=datetime.now(),
#             description="b",
#             location="b",
#         )).save()
#         test_event1.invitees.add(test_profile0)
#         test_event1.save()

#     def test_edit_my_event(self) -> None:
#         with driver_manager() as driver:
#             driver.get(f"{self.live_server_url}/")
#             generic_user_login(driver, "test_user0", "test_password")
#             driver.find_element(By.ID, "event-title-1").click()
#             self.assertEquals(
#                 len(driver.find_elements(By.ID, "edit-event")),
#                 1
#             )

#     def test_no_edit_not_my_event(self) -> None:
#         with driver_manager() as driver:
#             driver.get(f"{self.live_server_url}/")
#             generic_user_login(driver, "test_user0", "test_password")
#             driver.find_element(By.ID, "Invited Events Filter").click()
#             driver.find_element(By.ID, "event-title-1").click()
#             self.assertEquals(
#                 len(driver.find_elements(By.ID, "edit-event")),
#                 0
#             )

#     def test_default_dashboard_view(self) -> None:
#         with driver_manager() as driver:
#             # Log in to website
#             driver.get(f"{self.live_server_url}/")
#             generic_user_login(driver, "test_user0", "test_password")

#             # Make sure the current filter is for My Events
#             self.assertEquals(
#                 driver.find_element(By.ID, "Current Filter Mode").text,
#                 "The dashboard is currently in mode My Events"
#             )

#     def test_view_my_event(self) -> None:
#         with driver_manager() as driver:
#             # Log in to website
#             driver.get(f"{self.live_server_url}/")
#             generic_user_login(driver, "test_user0", "test_password")

#             # Change view to My Event and make sure it works
#             driver.find_element(By.ID, "My Events Filter").click()
#             self.assertEquals(
#                 driver.find_element(By.ID, "Current Filter Mode").text,
#                 "The dashboard is currently in mode My Events"
#             )
#             # Make sure there is only one event
#             self.assertEquals(
#                 len(driver.find_elements(By.TAG_NAME, "a")),
#                 1
#             )
#             # Make sure that event has the same name as the one this user owns
#             self.assertEquals(
#                 driver.find_element(By.ID, "event-title-1").text,
#                 "a"
#             )

#     def test_view_invited_event(self) -> None:
#         with driver_manager() as driver:
#             # Log in to website
#             driver.get(f"{self.live_server_url}/")
#             generic_user_login(driver, "test_user0", "test_password")

#             # Change view to My Event and make sure it works
#             driver.find_element(By.ID, "Invited Events Filter").click()
#             self.assertEquals(
#                 driver.find_element(By.ID, "Current Filter Mode").text,
#                 "The dashboard is currently in mode Invited Events"
#             )
#             # Make sure there is only one event
#             self.assertEquals(
#                 len(driver.find_elements(By.TAG_NAME, "a")),
#                 1
#             )
#             # Make sure that event has the same name as the one this user does not own
#             self.assertEquals(
#                 driver.find_element(By.ID, "event-title-1").text,
#                 "b"
#             )

#     def test_view_all_events(self) -> None:
#         driver: selenium.webdriver.Firefox  # TODO: REMOVE
#         with driver_manager() as driver:
#             # Log in to website
#             driver.get(f"{self.live_server_url}/")
#             generic_user_login(driver, "test_user0", "test_password")

#             # Change view to My Event and make sure it works
#             driver.find_element(By.ID, "All Events Filter").click()
#             self.assertEquals(
#                 driver.find_element(By.ID, "Current Filter Mode").text,
#                 "The dashboard is currently in mode All Events"
#             )
#             # Make sure there are two events
#             self.assertEquals(
#                 len(driver.find_elements(By.TAG_NAME, "a")),
#                 2
            # )

class TestLogout(StaticLiveServerTestCase):
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

    # user can logout
    def test_normal_logout(self) -> None:
        # test logging out
        with driver_manager() as driver:
            driver.get(f"{self.live_server_url}/")
            generic_user_login(driver, "test_user0", "test_password")
            driver.find_element(By.CLASS_NAME, "logoutbtn").click()
            self.assertEqual(
                len(driver.find_elements(By.ID, "id_new_account_button")),
                1
            )

    # user sees accept and decline buttons
    def test_accept_decline_event(self) -> None:
        with driver_manager() as driver:
            # Log in to website
            driver.get(f"{self.live_server_url}/")
            generic_user_login(driver, "test_user0", "test_password")
            # Change view to Attending Event and make sure it works
            driver.find_element(By.ID, "event-title-2").click()
            # Make sure there are two events
            self.assertEqual(
                len(driver.find_elements(By.ID, "accept")),
                1
            )

    # accept an invitation to an event
    def test_accept_event(self) -> None:
        with driver_manager() as driver:
            # Log in to website
            driver.get(f"{self.live_server_url}/")
            generic_user_login(driver, "test_user0", "test_password")
            # Change view to Attending Event and make sure it works
            driver.find_element(By.ID, "event-title-2").click()
            driver.find_element(By.ID, "accept").click()
            # Make sure there are two events
            self.assertEqual(
                len(driver.find_elements(By.ID, "event-title-2")),
                1
            )

    # declines event
    def test_decline_event(self) -> None:
        with driver_manager() as driver:
            # Log in to website
            driver.get(f"{self.live_server_url}/")
            generic_user_login(driver, "test_user0", "test_password")
            # Change view to Attending Event and make sure it works
            driver.find_element(By.ID, "event-title-2").click()
            driver.find_element(By.ID, "decline").click()
            # Make sure there are two events
            self.assertEqual(
                len(driver.find_elements(By.ID, "event-title-2")),
                0
            )

    # invites an invalid user
    def test_invite_person_no(self) -> None:
        with driver_manager() as driver:
            driver.get(f"{self.live_server_url}/")
            generic_user_login(driver, "test_user0", "test_password")
            driver.find_element(By.ID, "event-title-1").click()
            driver.find_element(By.ID, "edit-event").click()
            driver.find_element(By.ID, "Invite Button").click()
            driver.find_element(By.ID, "id_user_name").send_keys("jefferson")
            driver.find_element(By.ID, "invite them").click()
            # Make sure there are two events
            self.assertEqual(
                driver.find_element(By.ID, "not there").text,
                "'jefferson' is not a registered user."
            )

    # invites a valid user once
    def test_invite_valid_user(self) -> None:
        with driver_manager() as driver:
            driver.get(f"{self.live_server_url}/")
            generic_user_login(driver, "test_user0", "test_password")
            driver.find_element(By.ID, "event-title-1").click()
            driver.find_element(By.ID, "edit-event").click()
            driver.find_element(By.ID, "Invite Button").click()
            driver.find_element(By.ID, "id_user_name").send_keys("test_user1")
            driver.find_element(By.ID, "invite them").click()
            self.assertEqual(
                len(driver.find_elements(By.ID, "remove")),
                1
            )

    # invites the same person twice
    def test_invite_valid_user_two(self) -> None:
        with driver_manager() as driver:
            driver.get(f"{self.live_server_url}/")
            generic_user_login(driver, "test_user0", "test_password")
            driver.find_element(By.ID, "event-title-1").click()
            driver.find_element(By.ID, "edit-event").click()
            driver.find_element(By.ID, "Invite Button").click()
            driver.find_element(By.ID, "id_user_name").send_keys("test_user1")
            driver.find_element(By.ID, "invite them").click()
            driver.find_element(By.ID, "id_user_name").send_keys("test_user1")
            driver.find_element(By.ID, "invite them").click()
            self.assertEqual(
                len(driver.find_elements(By.ID, "remove")),
                1
            )
