import unittest

import django.db.models
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from planner.models import Profile, Event, Role
from Tests.DatabaseSafeTest import DatabaseSafeTest

from Tests.SeleniumSetUp import driver_manager, test_user_login


class RolesAdditionTest(DatabaseSafeTest):
    @classmethod
    def setUpClass(cls) -> None:
        user_owner = User()
        user_owner_profile = Profile()
        user_non_owner = User()
        user_non_owner_profile = Profile()
        event = Event()

    def tearDownClass(cls) -> None:
        pass

    def test_add_role_owner(self):
        pass

    def test_add_role_not_owner(self):
        pass
