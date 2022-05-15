import copy
from binarytree import Node
from typing import Dict, Set, Tuple
from AlgebraicExpressionParser.exceptions.Exceptions import *


class Expression:
    """An algebraic expression parser."""

    def __init__(self, *,
                 expression: str,
                 operators: Set[str],
                 operands: Set[str] = None,
                 operators_info: Dict[str, Tuple[int, int]],
                 unwritten_operator: str = None
                 ) -> None:
        """
        expression: A string that represents the expression.
        operators: A set of strings (a single character each) that represents the operators in the expression.
        operands: A set of strings (a single character each) that represents the operands in the expression.
        operators_info: A dictionary, where each key is an operator, and each value is a tuple. The tuple consists of two integers, the first is the operator's type (unary (1) or binary(2)), and the second is the operator's precedence. Example: {'+' : (1,3)}
        unwritten_operator: A string that represents an operator that is usually not written in the expression like the multiplication operator "*" in elementary algebra.
        """
        expression = self._remove_spaces_from_expression(expression)
        self.expression = expression
        self.operators = copy.copy(operators)
        self.operands = copy.copy(operands)
        self.operators_info = copy.deepcopy(operators_info)
        self.unwritten_operator = unwritten_operator

        if self.unwritten_operator:
            if self.unwritten_operator not in self.operators:
                raise InvalidUnwrittenOperatorException(
                    f"{self.unwritten_operator} is not a valid operator.")
            self._insert_operator()
        self.validate()

    @property
    def expression(self) -> str:
        return self._expression

    @expression.setter
    def expression(self, expression: str) -> None:
        if isinstance(expression, str):
            self._expression = expression
        else:
            raise TypeError(
                f"expression has to be an str. {expression} is {type(expression)}, not an str.")

    @property
    def operators(self) -> set:
        return self._operators

    @operators.setter
    def operators(self, operators: set) -> None:
        if isinstance(operators, set):
            self._operators = operators
        else:
            raise TypeError(
                f"operators has to be a set. {operators} is {type(operators)}, not a set.")

    @property
    def operands(self) -> set:
        return self._operands

    @operands.setter
    def operands(self, operands: set) -> None:
        if isinstance(operands, set) or operands == None:
            self._operands = operands
        else:
            raise TypeError(
                f"operands has to be a set. {operands} is {type(operands)}, not a set.")

    @property
    def operators_info(self) -> dict:
        return self._operators_info

    @operators_info.setter
    def operators_info(self, operators_info: dict) -> None:
        if isinstance(operators_info, dict):
            self._operators_info = operators_info
        else:
            raise TypeError(
                f"operators_info has to be a dict. {operators_info} is {type(operators_info)}, not a dict.")

    def __str__(self) -> str:
        return f"{self.expression}"

    def __repr__(self) -> str:
        return f"Expression('{self.expression}')"

    def is_binary_operator(self, c: str) -> bool:
        if c not in self.operators:
            return False
        return self.operators_info[c][0] == 2

    def is_unary_operator(self, c: str) -> bool:
        if c not in self.operators:
            return False
        return self.operators_info[c][0] == 1

    def is_operand(self, c: str) -> bool:
        if self.operands:
            return c in self.operands
        return not self.is_binary_operator(c) and not self.is_unary_operator(c) and not self._is_close_bracket(c) and not self._is_open_bracket(c)

    @staticmethod
    def _is_open_bracket(c: str) -> bool:
        return c == "(" or c == "[" or c == "{"

    @staticmethod
    def _is_close_bracket(c: str) -> bool:
        return c == ")" or c == "]" or c == "}"

    @staticmethod
    def _remove_spaces_from_expression(expression: str) -> str:
        expression = expression.replace("\n", "").replace(" ", "")
        return expression

    @staticmethod
    def _insert(string: str, index: int, c: str) -> str:
        return string[:index] + c + string[index:]

    @staticmethod
    def _are_pairs(c1: str, c2: str) -> bool:
        """Return True if the two brackets are the same type."""
        if c2 == "}" and c1 == "{":
            return True
        elif c2 == ")" and c1 == "(":
            return True
        elif c2 == "]" and c1 == "[":
            return True
        return False

    def _calc_weight(self, c: str) -> int:
        return self.operators_info[c][1]

    def _has_higher_precedence(self, c1: str, c2: str) -> bool:
        return self._calc_weight(c1) > self._calc_weight(c2)

    def _validate_operators_info(self) -> None: 
        """Raise an error if operators' info are not valid."""
        for operator in self.operators:
            if not isinstance(operator, str) or len(operator) != 1:
                raise InvalidOperatorException(
                    f"{operator} is not valid. has to be be an str and a single character.")
            if operator not in self.operators_info.keys():
                raise MissingOperatorsInfoException(
                    f"{self.expression} operators' info are missing.")
            else:
                if not isinstance(self.operators_info[operator], tuple):
                    raise TypeError(
                        f"operators_info[key] has to be a tuple. {self.operators_info[operator]} is {type(self.operators_info[operator])}, not tuple.")
                else:
                    if len(self.operators_info[operator]) != 2:
                        raise MissingOperatorsInfoException(
                            f"{self.expression} operators' info is missing.")
                    else:
                        if self.operators_info[operator][0] not in [1, 2]:
                            raise InvalidOperatorTypeException(
                                f"{operator}'s type is not valid. it has to be (2)-> binary or (1)-> unary.")
                        if not isinstance(self.operators_info[operator][1], int):
                            raise TypeError(
                                f"{operator}'s precedence has to be an int. {self.operators_info[operator][1]} is {type(self.operators_info[operator][1])} not an int.")

    def _validate_parenthesis(self) -> None:
        """Raise an error if expression's parenthesis are not valid."""
        stack = []
        for c in self.expression:
            if self._is_open_bracket(c):
                stack.append(c)
            elif self._is_close_bracket(c):
                if not stack:
                    raise InvalidParenthesesException(
                        f"{self.expression}'s parenthesis are not balanced.")
                if self._are_pairs(stack[-1], c):
                    stack.pop()
                else:
                    raise InvalidParenthesesException(
                        f"{self.expression}'s parenthesis are not balanced.")
        if stack:
            raise InvalidParenthesesException(
                f"{self.expression}'s parenthesis are not balanced.")

    def _validate_Expression(self, expression: str) -> None:
        """Raise an error if expression is not valid."""
        if expression == "":
            raise InvalidExpressionException(
                f"{self.expression} is not a valid expression.")
        sz = len(expression)
        is_previous_character_operand = False
        i = 0
        while i < sz:
            if self._is_open_bracket(expression[i]):
                if is_previous_character_operand:
                    raise InvalidExpressionException(
                        f"{self.expression} is not a valid expression.")
                open_brackets_count = 0
                idx = i

                # Find its close bracket
                while open_brackets_count != 1 or not Expression._is_close_bracket(expression[idx]):
                    if self._is_open_bracket(expression[idx]):
                        open_brackets_count += 1
                    if self._is_close_bracket(expression[idx]):
                        open_brackets_count -= 1
                    idx += 1
                    if idx >= sz:
                        raise InvalidParenthesesException(
                            f"{self.expression}'s parenthesis are not balanced.")

                self._validate_Expression(expression[i + 1: idx])

                i = idx
                is_previous_character_operand = True

            elif self._is_close_bracket(expression[i]):
                raise InvalidParenthesesException(
                    f"{self.expression}'s parenthesis are not balanced.")

            elif self.is_operand(expression[i]):
                if is_previous_character_operand:
                    raise InvalidExpressionException(
                        f"{self.expression} is not a valid expression.")
                is_previous_character_operand = True

            elif self.is_unary_operator(expression[i]):
                if not is_previous_character_operand:
                    raise InvalidExpressionException(
                        f"{self.expression} is not valid")

            elif self.is_binary_operator(expression[i]):
                if not is_previous_character_operand:
                    raise InvalidExpressionException(
                        f"{self.expression} is not a valid expression.")
                is_previous_character_operand = False

            i += 1
        if not is_previous_character_operand:
            raise InvalidExpressionException(
                f"{self.expression} is not a valid expression.")

    def validate(self) -> bool:
        """Return True if expression is valid."""
        self._validate_operators_info()
        self._validate_parenthesis()
        self._validate_Expression(self.expression)

        return True

    def postfix(self) -> str:
        """Return the postfix form for the expression."""
        postfix = ""
        operators_stack = []
        for c in self.expression:
            if self.is_operand(c):
                postfix += c
            elif self.is_binary_operator(c) or self.is_unary_operator(c):
                while operators_stack and not self._is_open_bracket(operators_stack[-1]) and self._has_higher_precedence(operators_stack[-1], c):
                    postfix += operators_stack[-1]
                    operators_stack.pop()
                operators_stack.append(c)
            elif self._is_open_bracket(c):
                operators_stack.append(c)
            elif self._is_close_bracket(c):
                while not self._is_open_bracket(operators_stack[-1]):
                    postfix += operators_stack[-1]
                    operators_stack.pop()
                operators_stack.pop()
        while operators_stack:
            postfix += operators_stack[-1]
            operators_stack.pop()
        return postfix
    
    def prefix(self) -> str:
        """Return the prefix form for the expression."""
        temp_expression = self.expression
        self.expression = self.expression[::-1]

        expression = ""
        for c in self.expression:
            if c == "(":
                expression += ")"
            elif c == ")":
                expression += "("
            else:
                expression += c
        self.expression = expression 
        prefix = self.postfix()[::-1]
        self.expression = temp_expression
        return prefix

    def tree(self) -> Node:
        """Return the expression tree."""
        postfix = self.postfix()
        stack = []
        for c in postfix:
            node = Node(c)
            if self.is_binary_operator(c):
                node.right = stack.pop()
                node.left = stack.pop()
            elif self.is_unary_operator(c):
                node.left = stack.pop()
            stack.append(node)
        return stack.pop()

    def _insert_operator(self) -> None:
        """insert an operator's symbol between operands. Example: ab(a) -> a&b&(a)."""
        i = 0
        while i < len(self.expression)-1:

            if self.is_operand(self.expression[i]) and (self.is_operand(self.expression[i+1]) or self._is_open_bracket(self.expression[i+1])):
                self.expression = self._insert(
                    self.expression, i+1, self.unwritten_operator)

            elif self._is_close_bracket(self.expression[i]) and (self.is_operand(self.expression[i+1]) or self._is_open_bracket(self.expression[i+1])):
                self.expression = self._insert(
                    self.expression, i+1, self.unwritten_operator)

            elif self.is_unary_operator(self.expression[i]) and (self.is_operand(self.expression[i+1]) or self._is_open_bracket(self.expression[i+1])):
                self.expression = self._insert(
                    self.expression, i+1, self.unwritten_operator)
            i += 1

    def update_operator_info(self, *, operator: str, operator_info: Tuple[int, int]) -> None:
        """Update the info of an operator."""
        self.operators_info[operator] = operator_info
        self.validate()
    
    def get_operands(self) -> set:
        """Return set that contains all symbols in the expression."""
        symbols = set()
        for c in self.expression:
            if self.is_operand(c):
                symbols.add(c)
        return symbols

    def get_binary_operators(self) -> set:
        """Return set that contains all the binary operators in the expression."""
        binary_operators = {
            operator for operator in self.operators if self.is_binary_operator(operator)}
        return binary_operators

    def get_unary_operators(self) -> set:
        """Return set that contains all the unary operators in the expression."""
        unary_operators = {
            operator for operator in self.operators if self.is_unary_operator(operator)}
        return unary_operators

    def get_operators(self) -> set:
        """Return set that contains all the operators in the expression."""
        operators = self.get_binary_operators()
        operators.update(self.get_unary_operators())
        return operators

    def get_operator_info(self, operator: str) -> Tuple[int, int]:
        """Return the info of an operator."""
        return self.operators_info[operator]

    def add_operator(self) -> None:
        raise NotImplementedError

    def add_operand(self) -> None:
        raise NotImplementedError
