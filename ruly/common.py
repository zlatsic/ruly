import abc
from collections import namedtuple
import enum


class Rule(namedtuple('Rule', ['antecedent', 'consequent'])):
    """Knowledge base rule

    Attributes:
        antecedent (Union[ruly.Condition, ruly.Expression]): expression or a
            condition that, if evaluated to True, fires assignment defined by
            the consequent
        consenquent (ruly.Assignment): represents an assignment of a value to a
            variable name
    """


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


class Assignment(namedtuple('Assignment', ['name', 'value'])):
    """Represents assignment of a value to a variable

    Attributes:
        name (str): variable name
        value (Any): assigned value
    """


class Unknown(namedtuple('Unknown', ['state', 'derived_name'])):
    """Structure representing unknown combination of state and
    derived variable.

    Attributes:
        state (Dict[str, Any]): all variable values
        derived_name (str): unknown derived variable"""


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
