import abc
from dataclasses import dataclass
import enum
from typing import Union, Dict, Any, List, Sequence


class Operator(enum.Enum):
    AND = 1


@dataclass
class Condition(abc.ABC):
    """Abstract class representing a condition that needs to be satisfied when
    evaluating an expression.

    Attributes:
        name (str): variable name
    """
    name: str

    @abc.abstractmethod
    def satisfied(self, value):
        """Checks whether the condition is satisfied for the given value

        Args:
            value (Any): checked value

        Returns:
            bool: true if condition is satisfied, false otherwise"""


@dataclass
class Expression:
    """Logical expression, aggregation of conditions and
    sub-expressions

    Attributes:
        operator (ruly.Operator): operator applied to all children when
            evaluated
        children (List[Union[ruly.Condition, ruly.Expression]]): list of
            conditions or other expressions
    """
    operator: Operator
    children: Sequence[Union[Condition, "Expression"]]

    def __str__(self):
        return f" {self.operator.name} ".join([str(c) for c in self.children])


@dataclass
class Rule:
    """Knowledge base rule

    Attributes:
        antecedent (Union[ruly.Condition, ruly.Expression]): expression or a
            condition that, if evaluated to True, fires assignment defined by
            the consequent.
        consequent (Dict[str, Any]): keys are variable names, values are
            values assigned if rule fires
    """
    antecedent: Union[Condition, Expression]
    consequent: Dict[str, Any]

    def __str__(self):
        consequent = " AND ".join(
            f"{k} = {v}" for k, v in self.consequent.items()
        )
        return f"IF {self.antecedent} THEN {consequent}"


def get_rule_depending_variables(rule):
    """Calculate all input variables in a rule

    Returns:
        List[str]: names of all input variables"""
    if isinstance(rule.antecedent, Condition):
        return {rule.antecedent.name}
    elif isinstance(rule.antecedent, Expression):
        return set([c.name for c in rule.antecedent.children])
