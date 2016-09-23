import unittest
from abc import ABCMeta

import httpretty
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

        # enable httpretty socket patch
        httpretty.enable()

        # configure the application
        brutus_module_weather.app.config['TESTING'] = True

        # create the test client
        self.app = brutus_module_weather.app.test_client()

    def tearDown(self):
        """
        Tear down the test case.
        """

        # disable httpretty socket patch
        httpretty.disable()

        # clear httpretty internal state
        httpretty.reset()

    def register_open_weather_map_urls(self):
        """
        Register API URLs for the Open Weather Map.
        """

        # math module
        httpretty.register_uri(
            httpretty.GET,
            "http://api.openweathermap.org/data/2.5/weather",
            body=json.dumps({
                "coord": {"lon": 145.77, "lat": -16.92},
                "weather": [
                    {
                        "id": 803,
                        "main": "Clouds",
                        "description": "broken clouds",
                        "icon": "04n"
                    }
                ],
                "base": "cmc stations",
                "main": {
                    "temp": 293.25,
                    "pressure": 1019,
                    "humidity": 83,
                    "temp_min": 289.82,
                    "temp_max": 295.37
                },
                "wind": {"speed": 5.1, "deg": 150},
                "clouds": {"all": 75},
                "rain": {"3h": 3},
                "dt": 1435658272,
                "sys": {
                    "type": 1,
                    "id": 8166,
                    "message": 0.0166,
                    "country": "AU",
                    "sunrise": 1435610796,
                    "sunset": 1435650870
                },
                "id": 2172797,
                "name": "Cairns",
                "cod": 200
            }),
            content_type="application/json")

    def parse_response(self, response):
        """
        Parse the response data as JSON and return it.
        """

        assert response.status_code == 200
        assert response.content_type == 'application/json'

        return json.loads(response.get_data()), response
