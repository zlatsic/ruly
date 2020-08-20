import abc
from collections import namedtuple
import enum


Rule = namedtuple('Rule', ['antecedent', 'consequent'])
Rule.__doc__ = """Knowledge base rule

Attributes:
    antecedent (Union[Condition, Expression]): expression or a condition that,
        if evaluated to True, fires assignment defined by the consequent
    consenquent (Assignment): represents an assignment of a value to a variable
        name
"""


class Operator(enum.Enum):
    AND = 1


Expression = namedtuple('Expression', ['operator', 'children'])
Expression.__doc__ = """Logical expression

Attributes:
    operator (Operator): operator applied to all children when evaluated
    children (List[Union[Condition, Expression]]): list of conditions or
        other expressions
"""


class Condition(abc.ABC):
    """Abstract class representing a condition that needs to be satisfied when
    evaluating an expression. Must have a name attribute.

    Attributes:
        name (str): name of the variable under which the condition is
            checked"""


EqualsCondition = namedtuple('EqualsCondition', ['name', 'value'])
Condition.register(EqualsCondition)
EqualsCondition.__doc__ = """Condition that checks wheter variable value is equal
to what is written in the condition

Attributes:
    name (str): variable name
    value (Any): value against which the variable is compared to
"""


Assignment = namedtuple('Assignment', ['name', 'value'])
Assignment.__doc__ = """Represents assignment of a value to a variable

Attributes:
    name (str): variable name
    value (Any): assigned value
"""


Unknown = namedtuple('Unknown', ['state', 'derived_name'])
Unknown.__doc__ = """Structure representing unknown combination of state and
derived variable.

Attributes:
    state (Dict[str, Any]): known variable values
    derived_name (str): unknown derived variable"""


def get_rule_depending_variables(rule):
    """Calculate all input variables in a rule

    Returns:
        List[str]: names of all input variables"""
    if isinstance(rule.antecedent, Condition):
        return set([rule.antecedent.name])
    elif isinstance(rule.antecedent, Expression):
        return set([c.name for c in rule.antecedent.children])
