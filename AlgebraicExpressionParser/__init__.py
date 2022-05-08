from expression import Expression


expression = Expression(expression="(1)*+00+0*", operators={'+', '&', '*'}, operators_info={'+': (2, 1), '&': (2, 2), '*': (1, 3)}, unwritten_operator='&')

print(expression.postfix())
print(expression.prefix())
print(expression.tree())