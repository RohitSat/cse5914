import unittest

from flask import json

from .common import BrutusTestCase


class TempuratureTestCase(BrutusTestCase):
    """
    Simple tests for the weather module
    Check that questions about temperature returns the correct answers
    """

    questions = ['Is it hot outside',
                 'Is it cold',
                 'What is the temperature',
                 'How hot is it']

    def test_basic_temperature_questions(self):
        """
        Ask a temperature question and
         make sure the answer is temperature related
        """

        # register open weather map URLs with generic data
        temp = 300
        fahrenheit = 80.33

        self.register_open_weather_map_urls(
            temp=temp, humidity=10, wind=10, clouds=45)

        for question in self.questions:
            answer = self.temperatureAnswer(fahrenheit)
            assert self.get_result(question) == answer, question
