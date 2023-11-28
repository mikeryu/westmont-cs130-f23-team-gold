import unittest
from random import getrandbits

import django.db.models


class DatabaseSafeTest(unittest.TestCase):
    random_test_id: str = str(getrandbits(64))
    persistent_test_dict: dict[str, django.db.models.Model] = dict()
    persistent_test_vars: list[django.db.models.Model] = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.random_test_id: str = str(getrandbits(64))
        cls.persistent_test_dict: dict[str, django.db.models.Model] = dict()
        cls.persistent_test_vars: list[django.db.models.Model] = []

    @classmethod
    def pushDjangoModel(cls, model: django.db.models.Model, name: str) -> django.db.models.Model:
        """
        pushDjangoModel is a utility to safely add a test record to our database.
        When a test record is added, if it successfully enters the database, it will be added to a stack of
        successfully entered test records.
        Then, when the test is done, the stack can be unwound and all the test records deleted from the database.

        :param name: the string by which this model should be accessible throughout the test.
        :param model: the test record to add to the database.
        :return: the model which was pushed.
        """
        try:
            if name in cls.persistent_test_dict.keys():
                raise KeyError("{:s} is already in the persistent test dictionary.".format(name))
            else:
                model.save()
                cls.persistent_test_dict[name] = model
        except Exception as e:
            cls.clearDjangoModels()
            raise e

        cls.persistent_test_vars.append(model)
        return model

    @classmethod
    def clearDjangoModels(cls) -> None:
        """
        clearDjangoModels is the counterpart of pushDjangoModel which allows the unwinding of the stack of
        test records in our database so that they may all be removed.
        If an exception is encountered while removing any record, this function will ignore the exception
        and continue to delete all the remaining records. It will then throw the first exception it encountered
        after it is finished deleting all remaining records.
        """
        error = None
        for model in reversed(cls.persistent_test_vars):
            try:
                model.delete()
            except Exception as e:
                if error is None:
                    print("Exception encountered while unwinding test model stack:")
                    error = e

        if error is not None:
            raise error

    @classmethod
    def __getitem__(cls, item: str) -> django.db.models.Model:
        """
        __getitem__ allows access to the static test variables of any test class,
        using the string name with which it was inserted in pushDjangoModel as the key.

        :param item: string key to attempt to access a model with
        :return: the model associated with that key in persistent_test_dict
        """
        try:
            return cls.persistent_test_dict.get(item)
        except KeyError as E:
            print("Did you forget to initialize {:s} as a test variable?".format(item))
            raise E

    @classmethod
    def tearDownClass(cls) -> None:
        """
        tearDownClass just makes sure that clearDjangoModels is called when a unit test is done.
        """
        cls.clearDjangoModels()
