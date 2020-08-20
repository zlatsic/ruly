from ruly import common


def backward_chain(knowledge_base, output_name,
                   resolve_conflict_cb=None, **kwargs):
    """Evaulates the output using backward chaining

    Args:
        knowledge_base (ruly.KnowledgeBase): knowledge base
        output_name (str): name of the output variable
        resolve_conflict_cb (Callable[List[ruly.Rule], Any]): function used to
            determine how value is calculated if multiple rules should fire at
            same variable, uses first found rule if None
        kwargs: names and values of input variables

    Returns:
        Tuple[Dict[str, Any], Set[ruly.Unknown]]: tuple containing evaluator
            state where keys are variable names and values are their values and
            list of found unknowns for which rules couldn't be applied"""
    state = {
        name: kwargs.get(name)
        for name in knowledge_base.input_variables.union(
            knowledge_base.derived_variables)}
    fired_rules = []
    unknowns = set()
    for rule in knowledge_base.rules:
        if rule.consequent.name != output_name:
            continue
        depending_variables = common.get_rule_depending_variables(rule)
        for variable in [var for var, value in depending_variables.items()
                         if value is not None]:
            if variable in knowledge_base.input_variables:
                # TODO handle missing inputs
                break
            state, new_unknowns = backward_chain(
                knowledge_base,
                variable,
                resolve_conflict_cb=resolve_conflict_cb,
                **state)
            unknowns |= new_unknowns
            if state[variable] is None:
                unknowns.add(common.Unknown(dict(state), output_name))
                break
            else:
                unknowns = set([unk for unk in unknowns
                                if unk.derived_name != variable])
        if evaluate(state, rule.antecedent):
            if resolve_conflict_cb is None:
                state[output_name] = rules.consequent.value
                return state, unknowns
            fired_rules.append(rule)

    if len(fired_rules) > 0:
        state[output_name] = resolve_conflict_cb(fired_rules)
    return state, unknowns


def evaluate(inputs, antecedent):
    """Evaluates an antecedent

    Args:
        inputs (Dict[str, Any]): variable values
        antecedent (Union[ruly.Expression, ruly.Condition]): rule
            antecedent

    Returns:
        bool"""
    if isinstance(antecedent, common.Condition):
        return _evaluate_condition(antecedent, inputs[antecedent.name])
    elif isinstance(antecedent, common.Expression):
        return _evaluate_expression(antecedent, inputs)


def _evaluate_expression(expression, inputs):
    if expression.operator == common.Operator.AND:
        return all([evaluate(inputs, child) for child in expression.children])


def _evaluate_condition(condition, input_value):
    if isinstance(condition, common.EqualsCondition):
        return condition.value == input_value
