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
               22341454: '22341454', 12335345345342: '12335345345342',
               0: 'zero', 1: 'one', 2: 'two', 10: 'ten',
               17: 'seventeen', 18: 'eighteen', 19: 'ninteen',
               50: 'fifty', 66: 'sixty six', 70: 'seventy',
               100: 'a hundred', 1000: 'thousand'}

    # test expressions with multiple operators
    # ex : a + b * d
    def test_complexExpressions(self):
        inputs = self.getNumberOperatorCombos()
        cases = self.addOperatorTerm(self.numbers, inputs)
        cases = self.addOperatorTerm(cases, inputs)

        for prefix in self.prefixes:
            for sym, text in cases.items():
                a = eval(sym)
                text = prefix + " " + text
                answer = "{} is {}".format(sym, a)
                assert self.get_result(text) == answer

    # create combinations of numbers and operators i
    # to make creating questions easier
    # ex : '+ 2'
    def getNumberOperatorCombos(self):
        inputs = {}
        for nDigit, nText in self.numbers.items():
            for opSym, opText in self.operators.items():
                symRep = "{} {}".format(opSym, nDigit)
                textRep = "{} {}".format(opText, nText)
                inputs[symRep] = textRep

        return inputs

    def addOperatorTerm(self, original, termToAdd):
        inputs = {}
        for oSym, oText in original.items():
            for nSym, nText in termToAdd.items():
                symRep = "{} {}".format(oSym, nSym)
                textRep = "{} {}".format(oText, nText)
                inputs[symRep] = textRep

        return inputs
