import unittest
import os

from .SeleniumSetUp import driver_manager


class TestDashboard(unittest.TestCase):
    def test_default_filter(self):
        with driver_manager() as driver:
            self.assertEquals("aaa", "aaa")

    def test_all_to_my(self):
        self.assertEquals(1, 2)

    def test_all_to_inv(self):
        self.assertEquals(2, 2)

    def test_my_to_all(self):
        self.assertEquals(2, 2)

    def test_my_to_inv(self):
        self.assertEquals(2, 2)

    def test_inv_to_all(self):
        self.assertEquals(2, 2)

    def test_inv_to_my(self):
        self.assertEquals(2, 2)
