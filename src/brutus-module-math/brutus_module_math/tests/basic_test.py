import unittest

from .common import BrutusTestCase


class BasicTestCase(BrutusTestCase):
    """
    A basic test case for creating and retrieving requests.
    """

    def test_create_request(self):
        """
        Create a new request and verify it contains an ID and the
        provided input data.
        """

        # create the request
        request_data = {'text': 'what is 1 plus 1'}
        create_data, create_response = self.parse_response(
            self.app.post(self.BRUTUS_API_REQUEST, data=request_data))

        # verify the request contains the input data
        assert hasattr(create_data, 'input')
        input_data = create_data['input']

        assert isinstance(input_data, dict)
        assert input_data == request_data
