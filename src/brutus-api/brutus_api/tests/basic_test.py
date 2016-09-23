import unittest

from flask import json

from .common import BrutusTestCase


class BasicTestCase(BrutusTestCase):
    """
    A basic test case for creating and retrieving requests.
    """

    REQUEST_SAMPLE_SIZE = 5

    def test_create_request(self):
        """
        Create a new request and verify it contains an ID and the
        provided input data.
        """

        # register module URLs with generic data
        self.register_common_urls()

        # create the request
        request_data = {'text': 'what is 1 plus 1'}
        create_data, create_response = self.parse_response(self.app.post(
            self.BRUTUS_API_REQUEST,
            data=json.dumps(request_data),
            content_type='application/json'))

        # verify the request contains a numeric id
        assert hasattr(create_data, 'id')
        request_id = create_data['id']

        assert isinstance(request_id, str)

        # verify the request contains the input data
        assert hasattr(create_data, 'input')
        input_data = create_data['input']

        assert isinstance(input_data, dict)
        assert input_data == request_data

        # retrieve the request
        retrieve_data, retrieve_response = self.parse_response(
            self.app.get(self.BRUTUS_API_REQUEST_BY_ID.format(id=request_id)))

        # verify the request contains a numeric id
        assert hasattr(retrieve_data, 'id')
        request_id = retrieve_data['id']

        assert isinstance(request_id, str)

        # verify the request contains the input data
        assert hasattr(retrieve_data, 'input')
        input_data = retrieve_data['input']

        assert isinstance(input_data, dict)
        assert input_data == request_data

    def test_unique_ids(self):
        """
        Create multiple new requests and verify they all have unique IDs.
        """

        # register module URLs with generic data
        self.register_common_urls()

        # create a few requests
        request_ids = set()
        for i in range(self.REQUEST_SAMPLE_SIZE):
            # create the request
            request_data = {'text': 'what is 1 plus 1'}
            create_data, create_response = self.parse_response(self.app.post(
                self.BRUTUS_API_REQUEST,
                data=json.dumps(request_data),
                content_type='application/json'))

            # keep track of the request id
            request_id = create_data['id']
            request_ids.add(request_id)

        # verify we have a unique id for each request we created
        assert len(request_ids) == self.REQUEST_SAMPLE_SIZE
