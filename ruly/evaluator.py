from ruly import common


def backward_chain(knowledge_base, output_name, post_eval_cb=None, **kwargs):
    """Evaulates the output using backward chaining

    The algorithm is depth-first-search, if goal variable assigment is
    contained within a rule that has a depending derived variable, this
    variable is solved for using the same function call.

    Args:
        knowledge_base (ruly.KnowledgeBase): knowledge base
        output_name (str): name of the goal variable
        post_eval_cb(Optional[Callable]): callback called after determining
            which rules fired, signature should match :func:`post_eval_cb`.
            Return value is changed state. If `None`, state is changed by using
            assignemnt of first fired rule's consequent (or not changed if no
            rules fired)
        **kwargs (Dict[str, Any]): names and values of input variables

    Returns:
        Dict[str, Any]: state containing calculated values
    """
    state = {
        name: kwargs.get(name)
        for name in knowledge_base.input_variables.union(
            knowledge_base.derived_variables)}
    if state[output_name] is not None:
        return state

    fired_rules = []
    for rule in [r for r in knowledge_base.rules
                 if output_name in r.consequent]:
        depending_variables = common.get_rule_depending_variables(rule)
        for depending_variable in [var for var in depending_variables
                                   if state[var] is None]:
            if depending_variable in knowledge_base.input_variables:
                break
            eval_state = backward_chain(knowledge_base, depending_variable,
                                        post_eval_cb=post_eval_cb, **state)
            state = dict(state, **eval_state)
            if state[depending_variable] is None:
                break
        if evaluate(state, rule.antecedent):
            if post_eval_cb is None:
                return dict(state, **rule.consequent)
            fired_rules.append(rule)

    if post_eval_cb:
        return post_eval_cb(state, output_name, fired_rules)
    return state


def post_eval_cb(state, output_name, fired_rules):
    """Placeholder function describing input and output arguments for the post
    evaluation callbacks

    Args:
        state (Dict[str, Any]): state calculated during evaluation
        output_name (str): name of the goal variable
        fired_rules (List[ruly.Rule]): rules whose antecedents were satisfied
            during the evaluation
    Returns:
        Dict[str, Any]: updated state"""


def evaluate(inputs, antecedent):
    """Evaluates truthiness of an antecedent

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
