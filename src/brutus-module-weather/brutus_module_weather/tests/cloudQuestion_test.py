import unittest

from flask import json

from .common import BrutusTestCase


class CloudTestCase(BrutusTestCase):
    """
    Simple tests for the weather module
    Check that questions about
        clouds return the correct answers
    """

    cloudQuestions = ['Is it cloudy',
                      'Are there a lot of clouds'
                      'How many clouds are there'
                      'hOW MANY CLOUDS ARE THere'
                      'Tell me about the clouds']

    def test_basic_clouds_questions(self):
        """
        Ask a cloud question and make sure the answer is cloud related
        """

        # register open weather map URLs with generic data
        cloud = 45
        self.register_open_weather_map_urls(
            temp=300, humidity=10, wind=10, clouds=cloud)

        for question in self.cloudQuestions:
            answer = self.cloudAnswer(cloud)
            assert self.get_result(question) == answer, question

    def test_lowCloudPercentage(self):
        """
        register low cloud percentage with open weather map
        make sure module returns 'The sky is clear'
        """

        # register open weather map URLs with generic data
        cloud = 5
        self.register_open_weather_map_urls(
            temp=300, humidity=10, wind=10, clouds=cloud)
        question = self.cloudQuestions[0]
        answer = self.cloudAnswer(cloud)
        assert self.get_result(question) == answer, question

    def test_mediumCloudPercentage(self):
        """
        register medium cloud percentage with open weather map
        make sure module returns 'There are scattered clouds'
        """

        # register open weather map URLs with generic data

        cloud = 40
        self.register_open_weather_map_urls(
            temp=300, humidity=10, wind=10, clouds=cloud)
        question = self.cloudQuestions[0]
        answer = self.cloudAnswer(cloud)
        assert self.get_result(question) == answer, question

    def test_highCloudPercentage(self):
        """
        register high cloud percentage with open weather map
        make sure module returns 'The sky is overcast'
        """

        # register open weather map URLs with generic data
        cloud = 95
        self.register_open_weather_map_urls(
            temp=300, humidity=10, wind=10, clouds=cloud)
        question = self.cloudQuestions[0]
        answer = self.cloudAnswer(cloud)
        assert self.get_result(question) == answer, question
