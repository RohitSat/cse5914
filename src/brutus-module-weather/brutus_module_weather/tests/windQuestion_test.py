import unittest

from flask import json

from .common import BrutusTestCase


class WindTestCase(BrutusTestCase):
    """
    Simple tests for the weather module
    Check that questions about wind returns the correct answers
    """

    windQuestions = ['Is it windy',
                     'is it WINDY',
                     'I bet there is a lot of wind today',
                     'I heard it is windy',
                     'Is the wind blowing hard']

    def test_basic_wind_questions(self):
        """
        Ask a wind question and make sure the answer is wind related
        """

        # register open weather map URLs with generic data
        wind = 10
        self.register_open_weather_map_urls(
            temp=300, humidity=10, wind=wind, clouds=45)

        for question in self.windQuestions:
            answer = self.windAnswer(wind)
            assert self.get_result(question) == answer, question
