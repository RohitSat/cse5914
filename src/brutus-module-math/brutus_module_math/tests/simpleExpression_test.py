import unittest

from flask import json

from .common import BrutusTestCase


class SimpleExpressionTestCase(BrutusTestCase):
    """
    Test case to check the response returned from the module
    Iterates through all of the prefixes, operators, and numbers for each
        operator type (add subtract, etc) to create simple questions
        ex: 'What is 1 + 1'
    """

    prefixes = ['what is', 'calculate', 'determine', '']
    addOp = ['+', 'plus', 'added to']
    subtractOp = ['-', 'minus']
    multiplicationOp = ['*', 'multiplied by', 'times']
    divisionOp = ['/', 'over', 'divided by']
    numbers = {1: '1', 22: '22', 234: '234', 6443: '6443', 32313: '32313',
               96678: '96678', 100000000000: '100000000000',
               22341454: '22341454', 12335345345342: '12335345345342',
               0: 'zero', 1: 'one', 2: 'two', 10: 'ten',
               11: 'eleven', 12: 'twelve', 13: 'thirteen',
               14: 'fourteen', 15: 'fifteen', 16: 'sixteen',
               17: 'seventeen', 18: 'eighteen', 19: 'ninteen',
               20: 'twenty', 30: 'thirty', 40: 'fourty',
               50: 'fifty', 60: 'sixty six', 70: 'seventy',
               80: 'eighty', 90: 'ninty', 200: 'two hundred',
               100: 'a hundred', 1000: 'thousand',
               10000: 'ten thousand', 1000000: 'billion'}

    def test_addition(self):
        sym = '+'
        for prefix in self.prefixes:
            for op in self.addOp:
                for n1Digit, n1Text in self.numbers.items():
                    for n2Digit, n2Text in self.numbers.items():
                        a = n1Digit + n2Digit
                        text = self.create_question(prefix, n1Text, n2Text, op)
                        answer = self.create_answer(n1Digit, n2Digit, sym, a)
                        assert self.get_result(text) == answer

    def test_subtraction(self):
        sym = '-'
        for prefix in self.prefixes:
            for op in self.subtractOp:
                for n1Digit, n1Text in self.numbers.items():
                    for n2Digit, n2Text in self.numbers.items():
                        a = n1Digit - n2Digit
                        text = self.create_question(prefix, n1Text, n2Text, op)
                        answer = self.create_answer(n1Digit, n2Digit, sym, a)
                        assert self.get_result(text) == answer

    def test_subtractedFrom(self):
        sym = '-'
        op = 'subtracted from'
        for prefix in self.prefixes:
            for n1Digit, n1Text in self.numbers.items():
                for n2Digit, n2Text in self.numbers.items():
                    a = n1Digit - n2Digit
                    text = self.create_question(prefix, n1Text, n2Text, op)
                    answer = self.create_answer(n1Digit, n2Digit, sym, a)
                    assert self.get_result(text) == answer

    def test_multiplication(self):
        sym = '*'
        for prefix in self.prefixes:
            for op in self.multiplicationOp:
                for n1Digit, n1Text in self.numbers.items():
                    for n2Digit, n2Text in self.numbers.items():
                        a = n1Digit * n2Digit
                        text = self.create_question(prefix, n1Text, n2Text, op)
                        answer = self.create_answer(n1Digit, n2Digit, sym, a)
                        assert self.get_result(text) == answer

    def test_division(self):
        sym = '/'
        for prefix in self.prefixes:
            for op in self.divisionOp:
                for n1Digit, n1Text in self.numbers.items():
                    for n2Digit, n2Text in self.numbers.items():
                        if n2Digit != 0:
                            a = n1Digit / n2Digit
                        else:
                            a = " undefined "
                        text = self.create_question(prefix, n1Text, n2Text, op)
                        answer = self.create_answer(n1Digit, n2Digit, sym, a)
                        assert self.get_result(text) == answer

    def create_question(self, prefix, num1, num2, op):
        return "{} {} {} {}".format(prefix, num1, op, num2)

    def create_answer(self, num1, num2, op, answer):
        return "{} {} {} is {}".format(num1, op, num2, answer)
