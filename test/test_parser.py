import pytest

import ruly


@pytest.mark.parametrize('input_str,expected', [
    ('IF rule_engine="ruly" THEN usability="awesome"',
     ruly.Rule(ruly.EqualsCondition('rule_engine', 'ruly'),
               {'usability': 'awesome'})),
    ('IF   rule_engine  =   "ruly"     THEN    usability   =   "awesome"',
     ruly.Rule(ruly.EqualsCondition('rule_engine', 'ruly'),
               {'usability': 'awesome'})),
    ('IF language="python" AND rule_engine="ruly" THEN usability="awesome"',
     ruly.Rule(
         ruly.Expression(
             ruly.Operator.AND,
             [ruly.EqualsCondition('language', 'python'),
              ruly.EqualsCondition('rule_engine', 'ruly')]),
         {'usability': 'awesome'})),
    ('IF language="python" AND rule_engine="ruly" THEN usability="awesome" '
     'AND life="good"',
     ruly.Rule(
         ruly.Expression(
             ruly.Operator.AND,
             [ruly.EqualsCondition('language', 'python'),
              ruly.EqualsCondition('rule_engine', 'ruly')]),
         {'usability': 'awesome', 'life': 'good'})),
    ('IF (language="python" AND weather="sunny") AND rule_engine="ruly" '
     'THEN usability="awesome"',
     ruly.Rule(
         ruly.Expression(
             ruly.Operator.AND,
             [ruly.Expression(
                 ruly.Operator.AND,
                 [ruly.EqualsCondition('language', 'python'),
                  ruly.EqualsCondition('weather', 'sunny')]),
              ruly.EqualsCondition('rule_engine', 'ruly')]),
         {'usability': 'awesome'})),
])
def test_parser(input_str, expected):
    rule = ruly.parse(input_str)
    assert rule == expected


def test_knowledge_base_parses():
    rule_str = 'IF rule_engine="ruly" THEN usability="awesome"'
    rule = ruly.parse(rule_str)
    knowledge_base = ruly.KnowledgeBase(rule_str)
    assert knowledge_base.rules == (rule, )
