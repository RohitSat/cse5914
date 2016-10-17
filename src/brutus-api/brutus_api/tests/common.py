import os
import unittest
import tempfile
from abc import ABCMeta

import redis
import responses
from flask import json, g
from rq import SimpleWorker, Queue
from rq.registry import StartedJobRegistry, FinishedJobRegistry
from watson_developer_cloud import NaturalLanguageClassifierV1, AuthorizationV1

import brutus_api
from brutus_api.database import connect_db, insert_db


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
        self.app.config['REDIS_DB'] = 1     # test redis database

        database_file, database_filename = tempfile.mkstemp()
        self.app.config['DATABASE'] = database_filename

        self.app.config['NLC_WATSON_USERNAME'] = 'error_if_not_present'
        self.app.config['NLC_WATSON_PASSWORD'] = 'error_if_not_present'
        self.app.config['NLC_CLASSIFIER_NAME'] = 'brutus_api'

        # connect to and initialize the database
        self.db = connect_db(self.app.config['DATABASE'])
        with self.app.open_resource('schema.sql', 'r') as schema_file:
            schema_sql = schema_file.read()

        self.db.executescript(schema_sql)
        self.db.commit()

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

        # disconnect from and delete the database
        self.db.close()
        os.remove(self.app.config['DATABASE'])

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

    def init_backend_modules(self):
        """
        Initialize common modules in the backend database.
        """

        # math module
        insert_db(
            self.db,
            'INSERT INTO module (name, url) VALUES (?, ?)',
            ('math', 'http://127.0.0.1:5010'))

        # weather module
        insert_db(
            self.db,
            'INSERT INTO module (name, url) VALUES (?, ?)',
            ('weather', 'http://127.0.0.1:5020'))

        # commit changes
        self.db.commit()

    def register_common_urls(self):
        """
        Register common URLs and their JSON responses for general testing.
        """

        self.register_bluemix_url()
        self.register_nlc_classify_url()
        self.register_math_module_urls()
        self.register_weather_module_urls()

    def register_bluemix_url(self):
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

    def register_nlc_classify_url(self, classes=None):
        if(classes is None):
            classes = [
                {'confidence': 0.92, 'class_name': 'math'},
                {'confidence': 0.08, 'class_name': 'weather'}
            ]

        responses.add(
            responses.POST,
            "".join([
                NaturalLanguageClassifierV1.default_url,
                '/v1/classifiers/TESTID/classify'
            ]),
            body=json.dumps({
                'classes': classes
            }),
            status=200,
            content_type='application/json')

    def register_math_module_urls(self, response=None):
        if(response is None):
            response = {
                "input": {"text": "what is 1 plus 1"},
                "output": {"text": "2"}
            }
        responses.add(
            responses.POST,
            "http://127.0.0.1:5010/api/request",
            body=json.dumps(response),
            status=200,
            content_type="application/json")

    def register_weather_module_urls(self, response=None):
        if(response is None):
            response = {
                "input": {"text": "what is the weather"},
                "output": {"text": "sunny"}
            }
        responses.add(
            responses.POST,
            "http://127.0.0.1:5020/api/request",
            body=json.dumps(response),
            status=200,
            content_type="application/json")

    def parse_response(self, response):
        """
        Parse the response data as JSON and return it.
        """

        assert response.status_code == 200
        assert response.content_type == 'application/json'

        return json.loads(response.get_data()), response
