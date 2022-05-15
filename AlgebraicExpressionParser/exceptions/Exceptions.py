
class InvalidExpressionException(Exception):
    """The expression is not valid. Some operators or operands are missing."""

    pass


class InvalidParenthesesException(Exception):
    """The parenthesis are not balanced in the expression."""

    pass


class MissingOperatorsInfoException(Exception):
    """The operator info is missing."""

    pass


class InvalidUnwrittenOperatorException(Exception):
    """The unwritten operator is not valid."""

    pass


class InvalidOperatorException(Exception):
    """The operator is not valid."""

    pass


class InvalidOperatorTypeException(Exception):
    """The operator type is not valid (not binary and not unary)."""

    pass
