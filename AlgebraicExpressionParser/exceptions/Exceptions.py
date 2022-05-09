
class InvalidExpressionException(Exception):
    """The expression is not valid. operators or operands are missing."""

    pass


class InvalidParenthesesException(Exception):
    """The expression's Parentheses is not balanced."""

    pass


class MissingOperatorsInfoException(Exception):
    """The expression operators's info are missing."""

    pass


class InvalidUnwrittenOperatorException(Exception):
    """The Unwritten operator is not valid."""

    pass


class InvalidOperatorException(Exception):
    """The operator is not valid."""

    pass


class InvalidOperatorTypeException(Exception):
    """The operator type is not valid. not binary or unary."""

    pass
