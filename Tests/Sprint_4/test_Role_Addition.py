import unittest

import django.db.models
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from planner.models import Profile, Event, Role

from Tests.SeleniumSetUp import driver_manager, test_user_login


class RolesAdditionTest(unittest.TestCase):
    persistent_test_vars = []

    @staticmethod
    def pushDjangoModel(model: django.db.models.Model) -> None:
        """
        pushDjangoModel is a utility to safely add a test record to our database.
        When a test record is added, if it successfully enters the database, it will be added to a stack of
        successfully entered test records.
        Then, when the test is done, the stack can be unwound and all the test records deleted from the database.

        :param model: the test record to add to the database
        """
        try:
            model.save()
        except Exception as e:
            RolesAdditionTest.clearDjangoModels()
            raise e

        RolesAdditionTest.persistent_test_vars.append(model)

    @staticmethod
    def clearDjangoModels() -> None:
        """
        clearDjangoModels is the counterpart of pushDjangoModel which allows the unwinding of the stack of
        test records in our database so that they may all be removed.
        If an exception is encountered while removing any record, this function will ignore the exception
        and continue to delete all the remaining records. It will then throw the first exception it encountered
        after it is finished deleting all remaining records.
        """
        error = None
        for model in reversed(RolesAdditionTest.persistent_test_vars):
            try:
                model.delete()
            except Exception as e:
                if error is None:
                    print("Exception encountered while unwinding test model stack:")
                    error = e

        if error is not None:
            raise error

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
