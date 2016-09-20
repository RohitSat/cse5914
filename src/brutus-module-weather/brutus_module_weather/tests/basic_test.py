import unittest

from .common import BrutusTestCase


class BasicTestCase(BrutusTestCase):
    """
    A basic test case for creating and retrieving requests.
    """

    def test_create_request(self):
        """
        Create a new request and verify it contains the
        provided input data and some output data.
        """

        # create the request
        request_data = {'text': 'what is the weather'}
        api_data, api_response = self.parse_response(
            self.app.post(self.BRUTUS_API_REQUEST, data=request_data))

        # verify the request contains the input data
        assert hasattr(api_data, 'input')
        input_data = api_data['input']

        assert isinstance(input_data, dict)
        assert input_data == request_data

        # verify the request contains output data
        assert hasattr(api_data, 'output')
        output_data = api_data['output']

        assert isinstance(output_data, dict)
        assert hasattr(output_data, 'text')
        assert isinstance(output_data['text'], str)
