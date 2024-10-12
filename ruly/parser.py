import json
import re
from ruly import common
from ruly import conditions


def parse(rule):
    """Parses a string representation of a rule and returns it. Uses JSON to
    deserialize values.

    Args:
        rule (str): string representation of a rule

    Returns:
        ruly.Rule"""

    if_antecedent_str, consequent_str = rule.split("THEN")
    antecedent_str = if_antecedent_str.split("IF")[1]
    return common.Rule(
        _parse_antecedent(antecedent_str), _parse_consequent(consequent_str)
    )


def _parse_antecedent(string):
    string = string.strip()
    parenth_regex = r"\((.+)\)"
    subexpressions = re.findall(parenth_regex, string)
    placeholders = []

    def repl(_):
        i = len(placeholders)
        placeholder = f"_subexpression{i}"
        while placeholder in string:
            i += 1
            placeholder = f"_subexpression{i}"
        placeholders.append(placeholder)
        return placeholder

    string = re.sub(parenth_regex, repl, string)

    op_locations = [(op, string.find(op.name)) for op in common.Operator]
    op = min(
        [(op, l) for op, l in op_locations if l != -1],
        key=lambda tup: tup[1],
        default=(None, 0),
    )[0]
    if op is None:
        if string == "_subexpression0":
            return _parse_antecedent(subexpressions[0])

        return _parse_condition(string)
    children = []
    for child_str in string.split(op.name):
        if "_subexpression" in child_str:
            child_str = child_str.strip()
            subexp_index = placeholders.index(child_str)
            child_str = subexpressions[subexp_index]
        children.append(_parse_antecedent(child_str))
    return common.Expression(op, children)


def _parse_consequent(string):
    consequent = {}
    for assignment in string.split("AND"):
        name, value_json = assignment.split("=", 2)
        consequent[name.strip()] = json.loads(value_json)
    return consequent


def _parse_condition(string):
    op = None
    cls = None
    if "<=" in string:
        op, cls = "<=", conditions.LessOrEqual
    elif ">=" in string:
        op, cls = ">=", conditions.GreaterOrEqual
    elif "<" in string:
        op, cls = "<", conditions.Less
    elif ">" in string:
        op, cls = ">", conditions.Greater
    elif "=" in string:
        op, cls = "=", conditions.Equals
    if op is None:
        raise ValueError(f"no operand found for condition {string}")
    name, value_json = string.split(op, 2)
    return cls(name.strip(), json.loads(value_json))


def _str_antecedent(antecedent):
    if isinstance(antecedent, common.Expression):
        return _str_expression(antecedent)
    return repr(antecedent)


def _str_expression(expression):
    child_strs = []
    for child in expression.children:
        if isinstance(child, common.Expression):
            child_strs.append(f"({_str_expression(child)})")
        elif isinstance(child, common.Condition):
            child_strs.append(str(child))
    return f" {expression.operator.name} ".join(child_strs)


def _str_consequent(assignment):
    return f'{assignment["name"]} = {json.dumps(assignment["value"])}'
