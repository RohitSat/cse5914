import unittest

from flask import json

from .common import BrutusTestCase


class ComplexExpressionTestCase(BrutusTestCase):
    """
    Test case to check the response returned from the module
    Iterates through all of the prefixes, operators, and numbers for each
        operator type (add subtract, etc) to create simple questions
        ex: 'What is 1 + 1'
    """

    prefixes = ['what is']
    operators = {'+': '+', '+': 'plus',
                 '-': '-', '-': 'minus',
                 '*': '*', '*': 'times',
                 '/': '/', '/': 'over'}
    numbers = {1: '1', 22: '22', 6443: '6443', 32313: '32313',
               17: 'seventeen', 18: 'eighteen', 19: 'ninteen',
               50: 'fifty', 66: 'sixty six', 70: 'seventy',
               100: 'a hundred', 1000: 'thousand'}

    """
    test expressions with multiple operators
    ex : a + b * c / d
    """
    def test_complexExpressions(self):
        # create combos for tests
        terms = self.addOperatorTerm(self.operators, self.numbers)
        cases = self.addOperatorTerm(self.numbers, terms)
        cases = self.addOperatorTerm(cases, terms)
        cases = self.addOperatorTerm(cases, terms)

        for prefix in self.prefixes:
            for sym, text in cases.items():
                a = eval(sym)
                text = prefix + " " + text
                answer = "{} is {}".format(sym, a)
                print(text)
                assert self.get_result(text) == answer, text

    """
    add together terms for question
    """
    def addOperatorTerm(self, first, second):
        inputs = {}
        for fSym, fText in first.items():
            for sSym, sText in second.items():
                symRep = "{} {}".format(fSym, sSym)
                textRep = "{} {}".format(fText, sText)
                inputs[symRep] = textRep

        return inputs
