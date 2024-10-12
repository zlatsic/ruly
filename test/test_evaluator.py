import ruly


def test_backward_chain():
    kb = ruly.KnowledgeBase(
        'IF sound="croak" AND behavior="eats flies" THEN animal="frog"',
        'IF sound="chirp" AND behavior="sings" THEN animal="canary"',
        'IF animal="frog" THEN color="green"',
        'IF animal="canary" THEN color="yellow"',
    )

    state = ruly.backward_chain(
        kb, "color", sound="croak", behavior="eats flies"
    )
    assert state["color"] == "green"

    state = ruly.backward_chain(kb, "color", sound="chirp", behavior="sings")
    assert state["color"] == "yellow"


def test_bc_post_eval():
    kb = ruly.KnowledgeBase(
        'IF sound="croak" AND behavior="eats flies" THEN animal="frog"',
        'IF sound="chirp" THEN animal="bird"',
        'IF sound="chirp" AND behavior="sings" THEN animal="canary"',
        'IF animal="frog" THEN color="green"',
        'IF animal="canary" THEN color="yellow"',
        'IF animal="bird" THEN color="n/a"',
    )

    def post_eval_cb(eval_state, output_name, fired_rules):
        if len(fired_rules) == 0:
            return dict(eval_state, **{output_name: "really n/a"})
        elif len(fired_rules) == 1:
            selected_rule = fired_rules[0]
        else:
            selected_rule = max(
                fired_rules,
                key=lambda r: len(ruly.get_rule_depending_variables(r)),
            )
        new_state = dict(eval_state)
        new_state.update(selected_rule.consequent)
        return new_state

    state = ruly.backward_chain(
        kb, "color", post_eval_cb=post_eval_cb, sound="chirp", behavior="sings"
    )
    assert state["color"] == "yellow"

    state = ruly.backward_chain(
        kb, "color", post_eval_cb=post_eval_cb, sound="chirp"
    )
    assert state["color"] == "n/a"

    state = ruly.backward_chain(
        kb, "color", post_eval_cb=post_eval_cb, sound="roar"
    )
    assert state["color"] == "really n/a"


def test_numeric():
    kb = ruly.KnowledgeBase(
        'IF weight>=100 THEN animal="elephant"',
        'IF weight>=50 AND weight<100 THEN animal="horse"',
        'IF weight>=25 AND weight<50 THEN animal="dog"',
        'IF weight>0 AND weight<25 THEN animal="mouse"',
    )

    state = ruly.backward_chain(kb, "animal", weight=145)
    assert state["animal"] == "elephant"

    state = ruly.backward_chain(kb, "animal", weight=59)
    assert state["animal"] == "horse"

    state = ruly.backward_chain(kb, "animal", weight=37)
    assert state["animal"] == "dog"

    state = ruly.backward_chain(kb, "animal", weight=12)
    assert state["animal"] == "mouse"
