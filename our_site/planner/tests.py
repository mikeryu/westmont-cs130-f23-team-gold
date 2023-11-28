from django.test import TestCase
from planner.models import *


class SiteTest(TestCase):
    def setUp(self) -> None:
        testuser = User(username="test_user", password="test_password")
        testuser.save()

    def test_something(self) -> None:
        self.assertEquals(True, True)
        works = User.objects.get()
        self.assertEquals(works.username, "test_user")
