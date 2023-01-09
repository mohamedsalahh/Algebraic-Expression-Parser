# Algebraic-Expression-Parser
Control and handle any algebraic expression, as well as do common expression operations such as getting postfix, prefix, and expression tree.

# Requirements
- binarytree
```
pip install binarytree
```

## Installing
[`pip install Algebraic-Expression-Parser`](https://pypi.org/project/Algebraic-Expression-Parser/)

### Importing
```python
from AlgebraicExpressionParser import Expression
```


```python
expression = Expression(expression = "x+sin(90)^2*y", 
                        operators = {'+', 'sin', '^', '*'}, 
                        operators_info = {'+': (2, 1), '*': (2, 2),'^': (2, 3), 'sin': (1, 4)}, 
                        operators_associativity = {'+': 'LR', '*': 'LR','^': 'RL', 'sin': 'RL'},
                        variables = {'x', 'y'})
```

```python
expression.postfix()
```
```text
['x', '90', 'sin', '2', '^', 'y', '*', '+']
```

```python
expression.prefix()
```
```text
['+', 'x', '*', '^', 'sin', '90', '2', 'y']
```

```python
expression.tree()
```
```text
 +___________
 /            \
x            __*
            /   \
       ____^     y
      /     \
    sin      2
       \
        90
```

```python
expression.tree().inorder
```
```text
[Node(X), Node(+), Node(sin), Node(90), Node(^), Node(2), Node(*), Node(Y)]
```
