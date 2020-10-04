import ruly


def test_backward_chain():
    kb = ruly.KnowledgeBase(
        ruly.Rule(
            ruly.Expression(
                operator=ruly.Operator.AND,
                children=[
                    ruly.EqualsCondition(name='sound', value='croak'),
                    ruly.EqualsCondition(name='behavior', value='eats flies')
                ]),
            {'animal': 'frog'}),
        ruly.Rule(
            ruly.Expression(
                operator=ruly.Operator.AND,
                children=[
                    ruly.EqualsCondition(name='sound', value='chirp'),
                    ruly.EqualsCondition(name='behavior', value='sings')]),
            {'animal': 'canary'}),
        ruly.Rule(ruly.EqualsCondition(name='animal', value='frog'),
                  {'color': 'green'}),
        ruly.Rule(ruly.EqualsCondition(name='animal', value='canary'),
                  {'color': 'yellow'}))

    state = ruly.backward_chain(kb, 'color', sound='croak',
                                behavior='eats flies')
    assert state['color'] == 'green'

    state = ruly.backward_chain(kb, 'color', sound='chirp',
                                behavior='sings')
    assert state['color'] == 'yellow'
