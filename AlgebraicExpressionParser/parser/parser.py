from typing import List, Set, Tuple, Union
from collections import deque
import copy

from AlgebraicExpressionParser.exceptions.exceptions import *
from AlgebraicExpressionParser.parser.operators import Operators, Operator
from AlgebraicExpressionParser.parser.node import Node


escape_charcter = "$"


class ExpressionParser:
    """Algebraic expression parser."""

    def __init__(self, operators: Operators, *, special_variables: Union[List[str], Set[str]] = set()) -> None:
        """
        operators: represents operators rules.
            type: Operators
        special_variables: represents variables other than predefined ones(constants and one symbol variables).
            type: list or set
            default: empty set {}
        """
        self.operators = operators
        self.special_variables = special_variables

    @property
    def operators(self) -> Operators:
        return self._operators

    @operators.setter
    def operators(self, operators: Operators) -> None:
        if not isinstance(operators, Operators):
            raise TypeError(
                f"operators has to be an Operators instance. {operators} is {type(operators)}.")
        self._operators = operators

    @property
    def special_variables(self) -> Operators:
        return self._special_variables

    @special_variables.setter
    def special_variables(self, special_variables: Union[List[str], Set[str]]) -> None:
        if not isinstance(special_variables, (set, list)):
            raise TypeError(
                f"special_variables has to be a set. {special_variables} is {type(special_variables)}.")
        self._special_variables = set(copy.copy(special_variables))

    def __str__(self) -> str:
        return f"{self.operators}"

    def __repr__(self) -> str:
        return f"ExpressionParser({self.operators.__repr__()})"

    def is_operand(self, c: str) -> bool:
        return self._is_constant(c) or self._is_variable(c) or c in self.special_variables

    @staticmethod
    def _is_variable(c: str) -> bool:
        return c.isalpha() and len(c) == 1

    @staticmethod
    def _is_constant(c: str) -> bool:
        if len(c.strip()) != len(c) or c[0] == '+' or c[0] == '-' or c is None:
            return False
        try:
            float(c)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_open_bracket(c: str) -> bool:
        return c == "(" or c == "[" or c == "{"

    @staticmethod
    def is_close_bracket(c: str) -> bool:
        return c == ")" or c == "]" or c == "}"

    def _is_bracket(self, c: str) -> bool:
        return self.is_close_bracket(c) or self.is_open_bracket(c)

    @staticmethod
    def _are_pairs(bracket1: str, bracket2: str) -> bool:
        """Return True if the two brackets has the same type."""
        if bracket2 == "}" and bracket1 == "{":
            return True
        elif bracket2 == ")" and bracket1 == "(":
            return True
        elif bracket2 == "]" and bracket1 == "[":
            return True
        return False

    def _is_valid_token(self, token: str) -> bool:
        return self._is_bracket(token) or self.is_operand(token) or self.operators.is_operator(token) or token.isspace() or token == escape_charcter

    def _find_next_matching_token(self, expression: str, start_idx: int) -> Tuple[str, int]:
        token = ''
        accepted_lexeme = ''
        longest_idx = start_idx
        while start_idx < len(expression):
            token += expression[start_idx]
            if self._is_valid_token(token):
                accepted_lexeme = token
                longest_idx = start_idx
            start_idx += 1
        return (accepted_lexeme, longest_idx)

    def tokenize(self, expression: str) -> List[str]:
        """Split the expression into tokens"""
        idx = 0
        tokens = []
        while idx < len(expression):
            token, next_idx = self._find_next_matching_token(expression, idx)
            if not token:
                raise InvalidExpressionException(
                    "expression is not valid.")
            idx = next_idx + 1
            tokens.append(token)
        return tokens

    def _parse(self, tokens: List[str], tokens_postfix: List[str]) -> None:
        """validates expression tokens and constructs postfix form from given tokens."""
        if not tokens:
            raise InvalidExpressionException(
                "expression is not valid.")
        sz = len(tokens)
        operators_stack = deque()
        is_previous_character_operand = False
        i = 0
        while i < sz:
            if self.is_open_bracket(tokens[i]):
                if is_previous_character_operand:
                    raise InvalidExpressionException(
                        "expression is not valid.")
                open_brackets_count = 0
                idx = i
                # find its close bracket.
                while open_brackets_count != 1 or not self.is_close_bracket(tokens[idx]):
                    if tokens[idx] == escape_charcter:
                        idx += 1
                    elif self.is_open_bracket(tokens[idx]):
                        open_brackets_count += 1
                    elif self.is_close_bracket(tokens[idx]):
                        open_brackets_count -= 1
                    idx += 1
                    if idx >= sz:
                        raise InvalidParenthesesException(
                            "expression's parenthesis are not balanced.")
                if not self._are_pairs(tokens[i], tokens[idx]):
                    raise InvalidParenthesesException(
                        "expression's parenthesis are not balanced.")
                self._parse(tokens[i + 1: idx], tokens_postfix)

                i = idx
                is_previous_character_operand = True

            elif self.is_close_bracket(tokens[i]):
                raise InvalidParenthesesException(
                    "expression's parenthesis are not balanced.")

            elif tokens[i].isspace():
                i += 1
                continue

            elif tokens[i] == escape_charcter:
                if is_previous_character_operand:
                    raise InvalidExpressionException(
                        "expression is not valid.")
                is_previous_character_operand = True
                tokens_postfix.append(tokens[i])
                i += 1
                tokens_postfix.append(tokens[i])

            elif self.operators.is_operator(tokens[i]):
                unary_rule = binary_rule = None
                is_valid = False
                for rule in self.operators.get_operator_rules(tokens[i]):
                    if rule.type == Operator.unary:
                        unary_rule = rule
                    if rule.type == Operator.binary:
                        binary_rule = rule
                if unary_rule:
                    if (unary_rule.position == Operator.postfix and is_previous_character_operand) or (unary_rule.position == Operator.prefix and not is_previous_character_operand):
                        is_valid = True
                        binary_rule = None
                if binary_rule:
                    if is_previous_character_operand:
                        is_valid = True
                        unary_rule = None
                    is_previous_character_operand = False
                if not is_valid:
                    raise InvalidExpressionException(
                        "expression is not valid.")
                while operators_stack and self.operators.does_have_higher_precedence(operators_stack[-1][1], unary_rule if unary_rule else binary_rule):
                    tokens_postfix.append(operators_stack[-1][1])
                    operators_stack.pop()
                operators_stack.append(
                    (tokens[i], unary_rule if unary_rule else binary_rule))

            elif self.is_operand(tokens[i]):
                if is_previous_character_operand:
                    raise InvalidExpressionException(
                        "expression is not valid.")
                is_previous_character_operand = True
                tokens_postfix.append(tokens[i])

            else:
                raise InvalidExpressionException(
                    "expression is not valid.")
            i += 1
        if not is_previous_character_operand:
            raise InvalidExpressionException(
                "expression is not valid.")
        while operators_stack:
            tokens_postfix.append(operators_stack[-1][1])
            operators_stack.pop()

    def postfix(self, expression: str, include_operators_rules: bool = False) -> List[str]:
        """Return the postfix form for the expression."""
        if not isinstance(expression, str):
            raise TypeError(
                f"expression has to be str. {expression} is {type(expression)}, not str.")

        tokens = self.tokenize(expression)
        postfix = []
        self._parse(tokens, postfix)
        if not include_operators_rules:
            postfix = [c.symbol if isinstance(c, Operator) else c for c in postfix]
        return postfix

    def syntax_tree(self, expression: str) -> Node:
        """Return the expression syntax tree."""
        postfix = self.postfix(expression, include_operators_rules=True)
        stack = deque()
        i = 0
        while i < len(postfix):
            node = Node(postfix[i])
            if isinstance(postfix[i], Operator):
                node = Node(postfix[i].symbol)
                if postfix[i].type == Operator.unary:
                    if postfix[i].position == Operator.postfix:
                        if len(stack) < 1:
                            raise InvalidExpressionException(
                                "expression is not valid.")
                        node.left = stack.pop()
                    if postfix[i].position == Operator.prefix:
                        if len(stack) < 1:
                            raise InvalidExpressionException(
                                "expression is not valid.")
                        node.right = stack.pop()
                if postfix[i].type == Operator.binary:
                    if len(stack) < 2:
                        raise InvalidExpressionException(
                            "expression is not valid.")
                    node.right = stack.pop()
                    node.left = stack.pop()
            stack.append(node)
            i += 1
        return stack.pop()
