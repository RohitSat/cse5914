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

        # configure the application
        self.app = brutus_module_weather.app
        self.app.config['TESTING'] = True

        # create the test client
        self.client = self.app.test_client()

        # enable httpretty socket patch
        httpretty.enable()

    def tearDown(self):
        """
        Tear down the test case.
        """

        # disable httpretty socket patch
        httpretty.disable()
        httpretty.reset()

    def register_open_weather_map_urls(self, temp, humidity, wind, clouds):
        """
        Register API URLs for the Open Weather Map.
        """

        httpretty.register_uri(
            httpretty.GET,
            "http://api.openweathermap.org/data/2.5/weather?lang=en&id=524901",
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
                    "temp": temp,
                    "pressure": 1019,
                    "humidity": humidity,
                    "temp_min": 289.82,
                    "temp_max": 295.37
                },
                "wind": {"speed": wind, "deg": 150},
                "clouds": {"all": clouds},
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

    def get_result(self, question):
        request_data = {'input': {'text': question}}
        api_data, api_response = self.parse_response(self.client.post(
            self.BRUTUS_API_REQUEST,
            data=json.dumps(request_data),
            content_type='application/json'))

        output_data = api_data['output']
        return output_data['text']

    def cloudAnswer(self, cloudPercent):
        if(cloudPercent < 5):
            return "The sky is clear."
        elif(cloudPercent < 50):
            return "There are scattered clouds."
        elif(cloudPercent < 100):
            return "The sky is overcast."

    def windAnswer(self, wind):
        return "The wind speed is {} miles per hour.".format(wind)

    def humidityAnswer(self, humidity):
        return "The humidity is {} percent.".format(humidity)

    def weatherAnswer(self, weather):
        return "The current weather is {}".format(weather)

    def temperatureAnswer(self, temp):
        return "The current temperature is {} degrees fahrenheit.".format(temp)
