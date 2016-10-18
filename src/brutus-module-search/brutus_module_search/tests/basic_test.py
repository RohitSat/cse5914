import unittest

from flask import json

from .common import BrutusTestCase


class BasicTestCase(BrutusTestCase):
    """
    A basic test case for creating and retrieving requests.
    Ensure the json returned is formatted correctly
    """

    def test_create_request(self):
        """
        Create a new request and verify it contains the
        provided input data and some output data.
        """

        # create the request
        request_data = {'input': {'text': 'Who is taylor swift'}}
        api_data, api_response = self.parse_response(self.client.post(
            self.BRUTUS_API_REQUEST,
            data=json.dumps(request_data),
            content_type='application/json'))

        # verify the request contains the input data
        assert 'input' in api_data
        input_data = api_data['input']

        assert isinstance(input_data, dict)
        assert input_data == request_data['input']

        # verify the request contains output data
        assert 'output' in api_data
        output_data = api_data['output']

        assert isinstance(output_data, dict)
        assert 'text' in output_data
        assert isinstance(output_data['text'], str)
