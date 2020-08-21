Usage
=====

Installation
------------

To install ruly, call::

    pip install ruly

Quickstart
----------

Ruly's main use case can be summed up with the following code block:

.. code-block:: python

    import ruly

    knowledge_base = ruly.knowledge_base.create([
        "IF sound='croak' AND behavior='eats flies' THEN animal='frog'",
        "IF sound='chirp' AND behavior='sings' THEN animal='canary'",
        "IF animal='frog' THEN color='green'",
        "IF animal='canary' THEN color='yellow'"])
    evaluation = ruly.backward_chain(knowledge_base, 'color',
                                     sound='croak',
                                     behavior='eats flies')
    print(evaluation.state['color'])
    # prints green
    print(evaluation.state['animal'])
    # prints frog

We can see that there are two distinct separate steps taken in the usage -
knowledge base creation and evaluation. Optionally, since an evaluation result
also contains which variables couldn't be calculated, new rules can be
generated as a result, but the specifics of this are left to the implementation
that uses the library.

Knowledge base
--------------

The central point of the ruly's rule engine is a knowledge base. It serves as a
rule aggregator that evaluators use to derive other variable values. The
knowledge base is implemented in the following class:

.. autoclass:: ruly.KnowledgeBase
    :members:

Rule declaration
""""""""""""""""

Knowledge base requires a list of initial rules for creation and can add
additional rules after it's instantiated. Knowledge base's API is such that it
accepts both strings or :class:`ruly.Rule` objects. If strings are received,
they are parsed into :class:`ruly.Rule` objects, more on that in its separate
section. The object that represents the rule itself has the following signature:

.. autoclass:: ruly.Rule
    :members:

Rule's antecedent is a logical expression that, if evaluated to true, signifies
that rule should fire during evaluation. The consequent represents which value
will be added to a variable if the rule fires, represented through the
:class:`ruly.Assignment` class.

.. autoclass:: ruly.Assignment
    :members:

Conditions
''''''''''

.. autoclass:: ruly.Condition
    :members:

.. autoclass:: ruly.EqualsCondition
    :members:

Expressions
'''''''''''

.. autoclass:: ruly.Expression
    :members:


Evaluation
----------

Ruly offers evaluation functions for individual rules and knowledge bases.

.. autofunction:: ruly.backward_chain

.. autofunction:: ruly.evaluate