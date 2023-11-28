from datetime import datetime

from selenium.webdriver.common.by import By

from planner.models import *

from Tests.SeleniumSetUp import driver_manager, test_user_login
from Tests.DatabaseSafeTest import DatabaseSafeTest


class EventViewTest(DatabaseSafeTest):

    @classmethod
    def setUpClass(cls) -> None:
        """

        :return:
        """
        user1 = EventViewTest.pushDjangoModel(
            User(username="test_user_01" + EventViewTest.random_test_id),
            "test_user_01"
        )
        EventViewTest.pushDjangoModel(
            Profile(user=EventViewTest["test_user_01"]),
            "test_profile_01"
        )
        EventViewTest.pushDjangoModel(
            User(username="test_user_02" + EventViewTest.random_test_id),
            "test_user_02"
        )
        EventViewTest.pushDjangoModel(
            Profile(user=EventViewTest["test_user_02"]),
            "test_profile_02"
        )
        EventViewTest.pushDjangoModel(
            Event(
                owner=EventViewTest["test_user_01"],
                name="a",
                date=datetime.now(),
                description="a",
                location="a"
            ),
            "test_event_01"
        )
        event2 = EventViewTest.pushDjangoModel(
            Event(
                owner=EventViewTest["test_user_02"],
                name="a",
                date=datetime.now(),
                description="a",
                location="a"
            ),
            "test_event_02"
        )
        event2.invitees.add(user1)
        event2.save()

    def test_view_owned_event(self) -> None:
        """

        :return:
        """
        with driver_manager() as driver:
            driver.get("http://localhost:8000/")


    def test_view_invited_event(self) -> None:
        """

        :return:
        """
        pass
