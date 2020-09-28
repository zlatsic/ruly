import pytest

import ruly
from ruly import parser


@pytest.mark.skip()
@pytest.mark.parametrize("string,rule", [
    ('IF color = "red" THEN action = "stop"',
     ruly.Rule(ruly.EqualsCondition('color', 'red'),
               ruly.Assignment('action', 'stop')))
])
def test_parser(string, rule):
    assert parser.parse(string) == rule


@pytest.mark.parametrize("rule,string", [
    (ruly.Rule(ruly.EqualsCondition('color', 'red'),
               ruly.Assignment('action', 'stop')),
     'IF color = "red" THEN action = "stop"'),
    (ruly.Rule(ruly.Expression(ruly.Operator.AND,
                               [ruly.EqualsCondition('color', 'green'),
                                ruly.EqualsCondition('crowded', True)]),
               ruly.Assignment('action', 'stop')),
     'IF color = "green" AND crowded = true THEN action = "stop"'),
    (
        ruly.Rule(
            ruly.Expression(
                ruly.Operator.AND, [
                    ruly.EqualsCondition('color', 'green'),
                    ruly.Expression(ruly.Operator.AND, [
                        ruly.EqualsCondition('a', 1),
                        ruly.EqualsCondition('b', 2)])]),
            ruly.Assignment('action', 'stop')),
        'IF color = "green" AND (a = 1 AND b = 2) THEN action = "stop"'),
])
def test_repr(rule, string):
    assert parser.rule_str(rule) == string
