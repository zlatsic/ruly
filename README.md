# Ruly

Ruly is a simple, lightweight rule engine that can be used to define rules and
proove statements using backward chaining. It attempts to be highly
configurable, allowing callers of its functions to define callbacks in cases
for conflict resolutions or derivations of new rules.

## Installation

Ruly can be installed and used as a Python package. It can be installed by
calling:

```
pip install ruly
```

## Usage

```python
import ruly


knowledge_base = ruly.knowledge_base.create([
    "IF color = 'red' THEN creature = 'dragon'",
    "IF color = 'grey' THEN creature = 'rat'"])
print(ruly.backward_chain(knowledge_base, 'creature', color='red'))
# prints dragon
```

For more examples and information on how to create new rules, solve conflicts,
generate new rules on the fly during evaluations, etc., see the documentation.

## Development environment

To set up the development environment, ruly's build tool, `doit` needs to be
installed. Remaining tasks can be listed and executed using this tool.
