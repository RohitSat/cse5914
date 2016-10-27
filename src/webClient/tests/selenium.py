import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from flask import json

class seleniumTest(unittest.TestCase):
    """
    Simple test cases for the web client. Pls work.
    """
    def test_test(self):
      """
      Check if selenium is working as expected
      """
      driver = webdriver.Firefox()
      driver.get("http://www.google.com")
      assert "Google" in driver.title
