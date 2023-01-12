# Algebraic-Expression-Parser
Control and handle any algebraic expression, as well as do common expression operations such as getting postfix, prefix, and expression tree.


## Installing
[`pip install Algebraic-Expression-Parser`](https://pypi.org/project/Algebraic-Expression-Parser/)

### Importing
```python
from AlgebraicExpressionParser import ExpressionParser
from AlgebraicExpressionParser import Operator
from AlgebraicExpressionParser import Operators
```


```python
operators = [Operator(symbol='+'), Operator(symbol='-'), Operator(symbol='*', precedence=2), Operator(
    symbol='-', type=Operator.unary, precedence=3, associativity=Operator.rtl, position=Operator.prefix), Operator(symbol='^', precedence=4), Operator(symbol='sin', type=Operator.unary, precedence=3, associativity=Operator.rtl, position=Operator.prefix)]

operators = Operators(operators)

parser = ExpressionParser(operators)
```

```python
parser.postfix('(-3) * (x^3)')
```
```text
>>> ['3', '-', 'x', '3', '^', '*']
```

```python
parser.postfix('sin(x)--x')
```
```text
>>> ['x', 'sin', 'x', '-', '-']
```

```python
parser.postfix('1^2^3')
```
```text
>>> ['1', '2', '^', '3', '^']
```

```python
parser.postfix('1^(2^3)')
```
```text
>>> ['1', '2', '3', '^', '^']
```

```python
parser.syntax_tree('(-3) * (x^3)')
```
```text
>>> Node: (value: *, left: Node: (value: -, left: None, right: Node: (value: 3, left: None, right: None)), right: Node: (value: ^, left: Node: (value: x, left: None, right: None), right: Node: (value: 3, left: None, right: None)))
```

```python
parser.syntax_tree('(-3) * (x^3)').preorder()
```
```text
>>> ['*', '-', '3', '^', 'x', '3']
```
```python
parser.syntax_tree('(-3) * (x^3)').inorder()
```
```text
>>> ['-', '3', '*', 'x', '^', '3']
```

```python
parser.syntax_tree('(-3) * (x^3)').postorder()
```
```text
>>> ['3', '-', 'x', '3', '^', '*']
```


### New in version 0.0.4
#### Escape charcter ($)
- Any charcter after it will be handled as variable even if it is a space (only one character, for variables with more than one character use special_variables parameter).
- The characters after it has higher precedence than operators.
     
     
```python
parser.postfix('$+ + x')
```
```text
>>> ['$', '+', 'x', '+']
```
#### Special Variables
- A list represents variables other than predefined ones(constants and one symbol variables)
- They have lower precedence than operators.

```python
parser = ExpressionParser(operators, special_variables = {'_'})
```
```python
parser.postfix('_ * x')
```
```text
>>> ['_', 'x', '*']
```
    
    
