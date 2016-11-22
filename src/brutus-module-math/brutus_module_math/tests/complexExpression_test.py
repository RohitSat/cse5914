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
    operators = {
        '+': ['+', 'plus'],
        '-': ['-', 'minus'],
        '*': ['*', 'times'],
        '/': ['/', 'over']
    }
    nums = {1: '1', 22: '22', 6443: '6443', 32313: '32313',
               17: 'seventeen', 18: 'eighteen', 19: 'ninteen',
               50: 'fifty', 66: 'sixty six', 70: 'seventy',
               100: 'hundred', 1000: 'thousand'}

    """
    test expressions with multiple operators
    ex : a + b * c / d
    """
    def test_complexExpressions(self):
        # create combos for tests
        # how big to make the expression, measured via number of operators
        EXPRESSION_COMPLEXITY = 1
        expns = self.makeExpression(self.nums, self.operators, self.nums)
        for i in range(EXPRESSION_COMPLEXITY - 1):
            expns = self.makeExpression(expns, self.operators, self.nums)
        for prefix in self.prefixes:
            for sym, reps in expns.items():
                for rep in reps:
                    expected_result = eval(sym)
                    query = prefix + " " + rep
                    expected_response = "{} is {}".format(sym, expected_result)
                    try:
                        resp = self.get_result(query)
                        assert resp == expected_response, query
                    except:
                        print(query)

    """
    add together terms for question
    """
    def makeExpression(self, leftTerms, operators, rightTerms):
        inputs = {}
        for leftSym, leftText in leftTerms.items():
            for rightSym, rightText in rightTerms.items():
                for operatorSym, operatorTexts in operators.items():
                    symRep = "{} {} {}".format(leftSym, operatorSym, rightSym)
                    inputs[symRep] = []
                    for operator in operatorTexts:
                        textRep = "{} {} {}".format(
                            leftText,
                            operator,
                            rightText)
                        inputs[symRep].append(textRep)
        return inputs
