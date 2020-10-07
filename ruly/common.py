import abc
from collections import namedtuple
import enum
import json


class Rule(namedtuple('Rule', ['antecedent', 'consequent'])):
    """Knowledge base rule

    Attributes:
        antecedent (Union[ruly.Condition, ruly.Expression]): expression or a
            condition that, if evaluated to True, fires assignment defined by
            the consequent
        consenquent (Dict[str, Any]): keys are variable names, values are
            values assigned if rule fires
    """

    def __str__(self):
        consequent = ' AND '.join(
            f'{k} = {v}' for k, v in self.consequent.items())
        return f'IF {self.antecedent} THEN {consequent}'


class Operator(enum.Enum):
    AND = 1


class Expression(namedtuple('Expression', ['operator', 'children'])):
    """Logical expression, aggregation of conditions and
    sub-expressions

    Attributes:
        operator (ruly.Operator): operator applied to all children when
            evaluated
        children (List[Union[ruly.Condition, ruly.Expression]]): list of
            conditions or other expressions
    """

    def __str__(self):
        return f' {self.operator.name} '.join([str(c) for c in self.children])


class Condition(abc.ABC):
    """Abstract class representing a condition that needs to be satisfied when
    evaluating an expression."""


class EqualsCondition(namedtuple('EqualsCondition', ['name', 'value']),
                      Condition):
    """Condition that checks wheter variable value is
    equal to what is written under the value attribute

    Attributes:
        name (str): variable name
        value (Any): value against which the variable is compared to
    """

    def __str__(self):
        return f'{self.name} = {json.dumps(self.value)}'


class Evaluation(namedtuple('Evaluation', ['state', 'unknowns'])):
    """Structure representing an evaluation result

    Attributes:
        state (Dict[str, Any]: values): all variable values
        unknowns (Set[Unknown]): set of all found unknowns"""


def get_rule_depending_variables(rule):
    """Calculate all input variables in a rule

    Returns:
        List[str]: names of all input variables"""
    if isinstance(rule.antecedent, Condition):
        return set([rule.antecedent.name])
    elif isinstance(rule.antecedent, Expression):
        return set([c.name for c in rule.antecedent.children])
