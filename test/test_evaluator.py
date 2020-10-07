import ruly


def test_backward_chain():
    kb = ruly.KnowledgeBase(
        'IF sound="croak" AND behavior="eats flies" THEN animal="frog"',
        'IF sound="chirp" AND behavior="sings" THEN animal="canary"',
        'IF animal="frog" THEN color="green"',
        'IF animal="canary" THEN color="yellow"')

    state = ruly.backward_chain(kb, 'color', sound='croak',
                                behavior='eats flies')
    assert state['color'] == 'green'

    state = ruly.backward_chain(kb, 'color', sound='chirp',
                                behavior='sings')
    assert state['color'] == 'yellow'


def test_bc_post_eval():
    kb = ruly.KnowledgeBase(
        'IF sound="croak" AND behavior="eats flies" THEN animal="frog"',
        'IF sound="chirp" THEN animal="bird"',
        'IF sound="chirp" AND behavior="sings" THEN animal="canary"',
        'IF animal="frog" THEN color="green"',
        'IF animal="canary" THEN color="yellow"',
        'IF animal="bird" THEN color="n/a"')

    def post_eval_cb(state, output_name, fired_rules):
        if len(fired_rules) == 0:
            return dict(state, **{output_name: 'really n/a'})
        elif len(fired_rules) == 1:
            selected_rule = fired_rules[0]
        else:
            selected_rule = max(
                fired_rules,
                key=lambda r: len(ruly.get_rule_depending_variables(r)))
        new_state = dict(state)
        new_state.update(selected_rule.consequent)
        return new_state

    state = ruly.backward_chain(kb, 'color', post_eval_cb=post_eval_cb,
                                sound='chirp', behavior='sings')
    assert state['color'] == 'yellow'

    state = ruly.backward_chain(kb, 'color', post_eval_cb=post_eval_cb,
                                sound='chirp')
    assert state['color'] == 'n/a'

    state = ruly.backward_chain(kb, 'color', post_eval_cb=post_eval_cb,
                                sound='roar')
    assert state['color'] == 'really n/a'
