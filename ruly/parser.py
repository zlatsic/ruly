import json
import re
from ruly import common


def parse(rule_str):
    """Parses a string representation of a rule and returns it

    Args:
        rule_str (str): string representation of a rule

    Returns:
        ruly.Rule"""

    raise NotImplementedError()
    if_antecedent_str, consequent_str = rule_str.split('THEN')
    antecedent_str = if_antecedent_str.split('IF')[1]
    return common.Rule(_parse_antecedent(antecedent_str),
                       _parse_consequent(consequent_str))


def rule_str(rule):
    """Returns a human-readable rule representation

    Args:
        rule (ruly.Rule): rule

    Returns:
        str"""
    return (f'IF {_repr_antecedent(rule.antecedent)} '
            f'THEN {_repr_consequent(rule.consequent)}')


def _parse_antecedent(string):
    raise NotImplementedError()
    string = string.strip()
    parenth_regex = r'\((.+)\)'
    subexpressions = re.findall(parenth_regex, string)

    def repl(m):
        for i, _ in enumerate(subexpressions):
            yield f'_subexpression{i}'
    string = re.sub(parenth_regex, repl, string)

    op_locations = [(op, string.find(op.name)) for op in common.Operator]
    op = min([(op, l) for op, l in op_locations if l != -1],
             key=lambda tup: tup[1], default=None)
    if op is None:
        if string == '_subexpression0':
            return _parse_antecedent(subexpressions[0])

        # return _parse_condition(string)
        return None
    children = []
    for child_str in string.split(op.name):
        if '_subexpression' in child_str:
            subexp_index = int(child_str.split('_subexpression')[1])
            child_str = subexpressions[subexp_index]
        children.append(_parse_antecedent(child_str))
    return common.Expression(op, children)


def _parse_consequent(string):
    return common.Assignment(sub.strip() for sub in string.split('='))


def _repr_antecedent(antecedent):
    if isinstance(antecedent, common.Expression):
        return _repr_expression(antecedent)
    return repr(antecedent)


def _repr_expression(expression):
    child_reprs = []
    for child in expression.children:
        if isinstance(child, common.Expression):
            child_reprs.append(f'({_repr_expression(child)})')
        elif isinstance(child, common.Condition):
            child_reprs.append(repr(child))
    return f' {expression.operator.name} '.join(child_reprs)


def _repr_consequent(assignment):
    return f'{assignment.name} = {json.dumps(assignment.value)}'
