import unittest

from flask import json

from .common import BrutusTestCase

from ..nlc import Nlc


class NlcTestCase(BrutusTestCase):
    """
    Tests for the Natural language classifier wrapper class
    """

    def test_get_classifier(self):
        """
        Test that the Nlc wrapper class returns the correct
        classifier based on the percentages it is passed
        """

        classes = [
            {'confidence': .07, 'class_name': 'math'},
            {'confidence': .93, 'class_name': 'weather'}
        ]
        expected_classifier = 'weather'

        classifier_name = self.app.config['NLC_CLASSIFIER_NAME']

        # register module URLs with data
        self.register_bluemix_url()
        self.register_nlc_classify_url(classes)

        # create Nlc class
        nlc = Nlc(
            'username',
            'password',
            classifier_name)

        classifier = nlc.classify("This text doesn't actualy matter")

        assert classifier == expected_classifier

    def test_get_classifier_low_confidence(self):
        """
        Test that the Nlc wrapper class returns the correct
        classifier based on the percentages it is passed
        """

        classes = [
            {'confidence': .60, 'class_name': 'math'},
            {'confidence': .40, 'class_name': 'weather'}
        ]
        expected_classifier = 'weather'

        classifier_name = self.app.config['NLC_CLASSIFIER_NAME']

        # register module URLs with data
        self.register_bluemix_url()
        self.register_nlc_classify_url(classes)

        # create Nlc class
        nlc = Nlc(
            'username',
            'password',
            classifier_name)

        classifier = nlc.classify("This text doesn't actualy matter")

        assert classifier is 'None'
