from collections import namedtuple
import json

from ruly import common


class Equals(namedtuple('Equals', ['name', 'value']), common.Condition):
    """Condition that checks wheter variable value is equal to what is written
    under the value attribute

    Attributes:
        name (str): variable name
        value (Any): value against which the variable is compared to
    """

    def __str__(self):
        return f'{self.name} = {json.dumps(self.value)}'

    def satisfied(self, value):
        return value == self.value


class Greater(namedtuple('Greater', ['name', 'value']), common.Condition):
    """Condition that checks wheter variable value is greater than what is
    written under the value attribute

    Attributes:
        name (str): variable name
        value (Any): value against which the variable is compared to
    """

    def __str__(self):
        return f'{self.name} > {json.dumps(self.value)}'

    def satisfied(self, value):
        return value > self.value


class GreaterOrEqual(namedtuple('GreaterOrEqual', ['name', 'value']),
                     common.Condition):
    """Condition that checks wheter variable value is greater or equal to what
    is written under the value attribute

    Attributes:
        name (str): variable name
        value (Any): value against which the variable is compared to
    """

    def __str__(self):
        return f'{self.name} >= {json.dumps(self.value)}'

    def satisfied(self, value):
        return value >= self.value


class Less(namedtuple('Less', ['name', 'value']), common.Condition):
    """Condition that checks wheter variable value is less than what is
    written under the value attribute

    Attributes:
        name (str): variable name
        value (Any): value against which the variable is compared to
    """

    def __str__(self):
        return f'{self.name} < {json.dumps(self.value)}'

    def satisfied(self, value):
        return value < self.value


class LessOrEqual(namedtuple('LessOrEqual', ['name', 'value']),
                  common.Condition):
    """Condition that checks wheter variable value is less or equal to what
    is written under the value attribute

    Attributes:
        name (str): variable name
        value (Any): value against which the variable is compared to
    """

    def __str__(self):
        return f'{self.name} >= {json.dumps(self.value)}'

    def satisfied(self, value):
        return value <= self.value
