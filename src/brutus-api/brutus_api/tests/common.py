import unittest
from abc import ABCMeta

import httpretty
from flask import json

import brutus_api


class BrutusTestCase(unittest.TestCase, metaclass=ABCMeta):
    """
    A base class for test cases.
    """

    BRUTUS_API_REQUEST = '/api/request'
    BRUTUS_API_REQUEST_BY_ID = '/api/request/{id}'

    def setUp(self):
        """
        Set up the test case.
        """

        # enable httpretty socket patch
        httpretty.enable()

        # configure the application
        brutus_api.app.config['TESTING'] = True

        # create the test client
        self.app = brutus_api.app.test_client()

    def tearDown(self):
        """
        Tear down the test case.
        """

        # disable httpretty socket patch
        httpretty.disable()

        # clear httpretty internal state
        httpretty.reset()

    def register_common_urls(self):
        """
        Register common URLs and their JSON responses for general testing.
        """

        # math module
        httpretty.register_uri(
            httpretty.POST,
            "http://127.0.0.1:5010/api/request",
            body=json.dumps({
                "input": {"text": "what is 1 plus 1"},
                "output": {"text": "2"}
            }),
            content_type="application/json")

        # weather module
        httpretty.register_uri(
            httpretty.POST,
            "http://127.0.0.1:5020/api/request",
            body=json.dumps({
                "input": {"text": "what is the weather"},
                "output": {"text": "sunny"}
            }),
            content_type="application/json")

    def parse_response(self, response):
        """
        Parse the response data as JSON and return it.
        """

        assert response.status_code == 200
        assert response.content_type == 'application/json'

        return json.loads(response.get_data()), response
