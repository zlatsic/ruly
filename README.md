# Ruly

Ruly is a simple, lightweight rule engine that can be used to define rules and
prove statements using backward chaining. It attempts to be highly configurable,
allowing callers of its functions to define callbacks in cases for conflict
resolutions or derivations of new rules.

## Installation

Ruly can be installed and used as a Python (>=3.6) package. It can be installed by
calling:

```
pip install ruly
```

## Usage

```python
import ruly

knowledge_base = ruly.KnowledgeBase(
    'IF color = "red" THEN creature = "dragon"',
    'IF color = "grey" THEN creature = "rat"')
print(ruly.backward_chain(knowledge_base, 'creature', color='red'))
# prints dragon
```

For more examples and information on how to create new rules, solve conflicts,
generate new rules on the fly during evaluations, etc., see the
[documentation](https://ruly.readthedocs.io).

## Development environment

To set up the development environment, requirements must be installed either by
calling `setup.py` or by installing them manually using `pip` and
`requirements.txt` file. Also, ruly's build tool, [`doit`](https://pydoit.org/)
needs to be installed. Supported tasks can be listed by calling:

```bash
doit list
```

NOTE: Ruly's development environment is using Python 3.12, but since Ruly does
not require any runtime dependencies, the lowest supported version is Python
3.6. To test any new changes use the platform tests (`doit plat_test`) and
update the minor version if backwards compatibility is broken. Additionally,
there's CI support to test 3.7>, however 3.6 is not included in this because
GH actions we
