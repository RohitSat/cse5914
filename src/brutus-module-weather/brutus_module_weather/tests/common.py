import unittest
from abc import ABCMeta

from flask import json

import brutus_module_weather


class BrutusTestCase(unittest.TestCase, metaclass=ABCMeta):
    """
    A base class for test cases.
    """

    BRUTUS_API_REQUEST = '/api/request'

    def setUp(self):
        """
        Set up the test case.
        """

        # configure the application
        brutus_module_weather.app.config['TESTING'] = True

        # create the test client
        self.app = brutus_module_weather.app.test_client()

    def tearDown(self):
        """
        Tear down the test case.
        """

        # nothing to do
        pass

    def parse_response(self, response):
        """
        Parse the response data as JSON and return it.
        """

        assert response.status_code == 200
        assert response.content_type == 'application/json'

        return json.loads(response.get_data()), response
