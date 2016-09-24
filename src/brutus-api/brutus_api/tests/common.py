import unittest
from abc import ABCMeta

import redis
import responses
from flask import json, g
from rq import SimpleWorker, Queue
from rq.registry import StartedJobRegistry, FinishedJobRegistry
from watson_developer_cloud import NaturalLanguageClassifierV1, AuthorizationV1

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

        # configure the application
        self.app = brutus_api.app
        self.app.config['TESTING'] = True   # pass errors to test client
        self.app.config['REDIS_DB'] = 1     # test database
        self.app.config['NLC_WATSON_USERNAME'] = 'error_if_not_present'
        self.app.config['NLC_WATSON_PASSWORD'] = 'error_if_not_present'

        # create a redis connection pool
        self.redis_pool = redis.ConnectionPool(
            host=self.app.config['REDIS_HOST'],
            port=self.app.config['REDIS_PORT'],
            db=self.app.config['REDIS_DB'],
            max_connections=1)

        # create the redis client using the existing connection pool
        self.redis = redis.Redis(connection_pool=self.redis_pool)

        # delete all data from redis
        self.redis.flushall()

        # create the test client
        self.client = self.app.test_client()

        # enable requests module patch
        responses.start()

    def tearDown(self):
        """
        Tear down the test case.
        """

        # delete all data from redis
        self.redis.flushall()

        # disable requests module patch
        responses.stop()
        responses.reset()

    def process_jobs(self):
        """
        Run background tasks.
        """

        # create a request context
        with self.app.test_request_context('/'):
            # set up the request context
            self.app.preprocess_request()

            # create an in-process worker
            worker = SimpleWorker([g.queue], connection=g.queue.connection)

            # process jobs
            worker.work(burst=True)

    def register_common_urls(self):
        """
        Register common URLs and their JSON responses for general testing.
        """

        # bluemix
        responses.add(
            responses.GET,
            AuthorizationV1.default_url + '/v1/token',
            body='test',
            status=200,
            content_type='text/plain')

        responses.add(
            responses.GET,
            NaturalLanguageClassifierV1.default_url + '/v1/classifiers',
            body=json.dumps({
                'classifiers': [
                    {
                        'name': self.app.config['NLC_CLASSIFIER_NAME'],
                        'classifier_id': 'TESTID'
                    }
                ]
            }),
            status=200,
            content_type='application/json')

        responses.add(
            responses.POST,
            "".join([
                NaturalLanguageClassifierV1.default_url,
                '/v1/classifiers/TESTID/classify'
            ]),
            body=json.dumps({
                'classes': [
                    {'confidence': 90, 'class_name': 'math'}
                ]
            }),
            status=200,
            content_type='application/json')

        # math module
        responses.add(
            responses.POST,
            "http://127.0.0.1:5010/api/request",
            body=json.dumps({
                "input": {"text": "what is 1 plus 1"},
                "output": {"text": "2"}
            }),
            status=200,
            content_type="application/json")

        # weather module
        responses.add(
            responses.POST,
            "http://127.0.0.1:5020/api/request",
            body=json.dumps({
                "input": {"text": "what is the weather"},
                "output": {"text": "sunny"}
            }),
            status=200,
            content_type="application/json")

    def parse_response(self, response):
        """
        Parse the response data as JSON and return it.
        """

        assert response.status_code == 200
        assert response.content_type == 'application/json'

        return json.loads(response.get_data()), response
