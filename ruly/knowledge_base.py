from ruly import (common, parser)


class KnowledgeBase:
    """Class representing a knowledge base, stores known rules

    Args:
        rules (List[Union[ruly.Rule, str]]): initial rules of which the
            knowledge base consists, can be string representations
        parser(Callable[[str], ruly.Rule]): parser used to turn string
            representations into ruly.Rule objects, default is
            :meth:`ruly.parse`
    """

    def __init__(self, rules, parse=parser.parse):
        self._rules = []
        self._input_variables = set()
        self._derived_variables = set()
        self._parse = parse

        for rule in rules:
            if isinstance(rule, str):
                rule = self._parse(rule)
            self.add_rule(rule)

    @property
    def rules(self):
        """List[ruly.Rule]: Stored rules"""
        return self._rules

    @property
    def input_variables(self):
        """Set[str]: Names of variables that are never contained within a
            rule's antecedent"""
        return self._input_variables

    @property
    def derived_variables(self):
        """Set[str]: Names of variables contained within at least one rule's
            antecedent"""
        return self._derived_variables

    def add_rule(self, rule):
        """Add a new rule to the knowledge base. This can change which
        variables are considered input or derived

        Args:
            rule (Union[ruly.Rule, str]): rule or its string representation to
                add"""
        if isinstance(rule, str):
            rule = self._parse(rule)
        self._rules.append(rule)
        self._input_variables.update(common.get_rule_depending_variables(rule))
        self._derived_variables.add(rule.consequent.name)
        self._input_variables -= self._derived_variables
