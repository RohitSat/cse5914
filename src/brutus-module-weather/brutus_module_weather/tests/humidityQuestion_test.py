import unittest

from flask import json

from .common import BrutusTestCase


class HumidityTestCase(BrutusTestCase):
    """
    Simple tests for the weather module
    Check that questions about humdity returns the correct answers
    """

    humidQuestions = ['how humid is it',
                      'is it humid outside',
                      'what is the humidity like today?',
                      'I bet it is super humid outside.']

    def test_basic_humidity_questions(self):
        """
        Ask a humid question and make sure the answer is humid related
        """
        # register open weather map URLs with generic data
        temp = 300
        humidity = 10
        wind = 10
        cloud = 45
        self.register_open_weather_map_urls(temp, humidity, wind, cloud)

        for question in self.humidQuestions:
            answer = self.humidityAnswer(humidity)
            assert self.get_result(question) == answer, question
