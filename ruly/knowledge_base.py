from ruly import (common, parser)


class KnowledgeBase:
    """Class representing a knowledge base, stores known rules

    Args:
        *args (Tuple[Union[ruly.Rule, ruly.KnowledgeBase, str]]): initial rules
            of which the knowledge base consists, can be rule objects,
            knowledge bases or string representations
        parser(Callable[[str], ruly.Rule]): parser used to turn string
            representations into ruly.Rule objects, default is
            :meth:`ruly.parse`
    """

    def __init__(self, *args, parse=parser.parse):
        input_variables = set()
        derived_variables = set()
        rules = []
        for arg in args:
            if isinstance(arg, str):
                rules.append(parse(arg))
            elif isinstance(arg, KnowledgeBase):
                rules.extend(arg.rules)
            elif isinstance(arg, common.Rule):
                rules.append(arg)
            else:
                raise ValueError()
        for rule in rules:
            input_variables.update(common.get_rule_depending_variables(rule))
            derived_variables.update(rule.consequent)
            input_variables -= derived_variables

        self._rules = tuple(rules)
        self._input_variables = input_variables
        self._derived_variables = derived_variables
        self._parse = parse

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
