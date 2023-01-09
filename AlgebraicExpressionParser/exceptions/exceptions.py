class InvalidExpressionException(Exception):
    """The expression is not valid. Some operators or operands are missing."""

    pass


class InvalidParenthesesException(Exception):
    """The parenthesis are not balanced in the expression."""

    pass
