from ruly import common


def backward_chain(knowledge_base, output_name,
                   resolve_conflict_cb=None, order_rules_cb=None, **kwargs):
    """Evaulates the output using backward chaining

    The algorithm is depth-first-search, if goal variable assigment is
    contained within a rule that has a depending derived variable, this
    variable is solved for using the same function call.

    Args:
        knowledge_base (ruly.KnowledgeBase): knowledge base
        output_name (str): name of the goal variable
        resolve_conflict_cb (Optional[Callable[[List[ruly.Rule]], Any]]):
            function used to determine how value is calculated if multiple
            rules should fire at same variable, uses first found rule if None
        order_rules_cb(Optional[Callable[[Any, List[ruly.Rule]], List[ruly.Rule]]]):
            function used to determine order of evaluation of rules that assign
            the goal variable, uses order in knowledge base if None
        kwargs (Dict[str, Any]): names and values of input variables

    Returns:
        ruly.Evaluation: state and unknowns gathered evaluating inputs
    """  # NOQA
    state = {
        name: kwargs.get(name)
        for name in knowledge_base.input_variables.union(
            knowledge_base.derived_variables)}
    unknowns = set()
    if state[output_name] is not None:
        return common.Evaluation(state, unknowns)

    ordered_rules = [rule for rule in knowledge_base.rules
                     if rule.consequent.name == output_name]
    if order_rules_cb is not None:
        ordered_rules = order_rules_cb(ordered_rules)

    fired_rules = []
    for rule in ordered_rules:
        depending_variables = common.get_rule_depending_variables(rule)
        for depending_variable in [var for var in depending_variables
                                   if state[var] is None]:
            if depending_variable in knowledge_base.input_variables:
                # TODO handle missing inputs
                break
            dependancy_eval = backward_chain(
                knowledge_base,
                depending_variable,
                resolve_conflict_cb=resolve_conflict_cb,
                **state)
            unknowns |= dependancy_eval.unknowns
            state = dict(state, **dependancy_eval.state)
            if state[depending_variable] is None:
                unknowns.add(common.Unknown(dict(state), output_name))
                break
            else:
                unknowns = {unk for unk in unknowns
                            if unk.derived_name != depending_variable}
        if evaluate(state, rule.antecedent):
            if resolve_conflict_cb is None:
                state[output_name] = rule.consequent.value
                return common.Evaluation(state, unknowns)
            fired_rules.append(rule)

    if len(fired_rules) > 0:
        state[output_name] = resolve_conflict_cb(fired_rules)
    return common.Evaluation(state, unknowns)


def evaluate(inputs, antecedent):
    """Evaluates truthfulness of an antecedent

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
