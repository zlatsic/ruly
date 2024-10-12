import json
from dataclasses import dataclass
from typing import Any

from ruly import common


@dataclass
class Equals(common.Condition):
    """Condition that checks whether variable value is equal to what is written
    under the value attribute

    Attributes:
        value (Any): value against which the variable is compared to
    """
    value: Any

    def __str__(self):
        return f"{self.name} = {json.dumps(self.value)}"

    def satisfied(self, value):
        return value == self.value


@dataclass
class Greater(common.Condition):
    """Condition that checks whether variable value is greater than what is
    written under the value attribute

    Attributes:
        value (Any): value against which the variable is compared to
    """
    value: Any

    def __str__(self):
        return f"{self.name} > {json.dumps(self.value)}"

    def satisfied(self, value):
        return value > self.value


@dataclass
class GreaterOrEqual(common.Condition):
    """Condition that checks whether variable value is greater or equal to what
    is written under the value attribute

    Attributes:
        value (Any): value against which the variable is compared to
    """
    value: Any

    def __str__(self):
        return f"{self.name} >= {json.dumps(self.value)}"

    def satisfied(self, value):
        return value >= self.value


@dataclass
class Less(common.Condition):
    """Condition that checks whether variable value is less than what is
    written under the value attribute

    Attributes:
        value (Any): value against which the variable is compared to
    """
    value: Any

    def __str__(self):
        return f"{self.name} < {json.dumps(self.value)}"

    def satisfied(self, value):
        return value < self.value


@dataclass
class LessOrEqual(common.Condition):
    """Condition that checks whether variable value is less or equal to what
    is written under the value attribute

    Attributes:
        value (Any): value against which the variable is compared to
    """
    value: Any

    def __str__(self):
        return f"{self.name} >= {json.dumps(self.value)}"

    def satisfied(self, value):
        return value <= self.value
