import pytest

import ruly
from ruly import rule_parser


@pytest.mark.skip()
@pytest.mark.parametrize("string,rule", [
    ("IF color = 'red' THEN action = 'stop'",
     ruly.Rule(ruly.EqualsCondition('color', 'red'),
               ruly.Assignment('action', 'stop')))
])
def test_parser(string, rule):
    assert rule_parser.parse(string) == rule
