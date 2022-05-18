import copy
from binarytree import Node
from typing import Dict, List, Set, Tuple
from AlgebraicExpressionParser.exceptions.Exceptions import *


class Expression:
    """An algebraic expression parser."""

    def __init__(self, *,
                 expression: str,
                 operators: Set[str],
                 variables: Set[str] = None,
                 operators_info: Dict[str, Tuple[int, int]],
                 operators_associativity: Dict[str, str],
                 ) -> None:
        """
        expression: A string that represents the expression.
        operators: A set of strings (a single character each) that represents the operators in the expression.
        variables: A set of strings (a single character each) that represents the variables in the expression. Example X, Y, V
        operators_info: A dictionary, where each key is an operator, and each value is a tuple. The tuple consists of two integers, the first is the operator's type (unary (1) or binary(2)), and the second is the operator's precedence. Example: {'+' : (1,3)}
        operators_associativity: A dictionary, where each key is an operator, and each value is its associativity.
        """
        expression = self._remove_spaces_from_expression(expression)
        self.expression = expression
        self.operators = copy.copy(operators)
        self.variables = copy.copy(variables)
        self.operators_info = copy.deepcopy(operators_info)
        self.operators_associativity = copy.copy(operators_associativity)

        self._tokenize()
        self._validate()

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
    def variables(self) -> set:
        return self._variables

    @variables.setter
    def variables(self, variables: set) -> None:
        if isinstance(variables, set) or variables == None:
            self._variables = variables
        else:
            raise TypeError(
                f"variables has to be a set. {variables} is {type(variables)}, not a set.")
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
    @property
    def operators_associativity(self) -> dict:
        return self._operators_associativity

    @operators_associativity.setter
    def operators_associativity(self, operators_associativity: dict) -> None:
        if isinstance(operators_associativity, dict):
            self._operators_associativity = operators_associativity
        else:
            raise TypeError(
                f"unary_operators_associativity has to be a dict. {operators_associativity} is {type(operators_associativity)}, not a dict.")
    @property
    def tokens(self) -> List[str]:
        return self._tokens

    @tokens.setter
    def tokens(self, tokens: List[str]) -> None:
        self._tokens = tokens

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

    def is_variable(self, c: str) -> bool:
        if self.variables:
            return c in self.variables
        return False

    def is_operand(self, c: str) -> bool:
        if c.isdigit():
            return True
        return self.is_variable(c)

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
    def _are_pairs(bracket1: str, bracket2: str) -> bool:
        """Return True if the two brackets are the same type."""
        if bracket2 == "}" and bracket1 == "{":
            return True
        elif bracket2 == ")" and bracket1 == "(":
            return True
        elif bracket2 == "]" and bracket1 == "[":
            return True
        return False

    def _has_higher_precedence(self, operator1: str, operator2: str) -> bool:
        return self.operators_info[operator1][1] > self.operators_info[operator2][1]

    def _tokenize(self) -> None:
        """Split the expression into tokens"""

        separators = ['(', ')', '{', '}', '[', ']']
        separators.extend(self.get_operators())
        separators.sort(key=len, reverse=True)

        def separate(expression: List[str]) -> List[str]:
            for separator in separators:
                for i, subexpression in enumerate(expression):
                    if subexpression in separators:
                        continue

                    subexpression = subexpression.split(separator)

                    sz = len(subexpression)
                    idx = 1
                    while idx < sz:
                        subexpression.insert(idx, separator)
                        idx += 2
                        sz += 1

                    idx = i+1
                    for s in subexpression:
                        if s == '':
                            continue
                        expression.insert(idx, s)
                        idx += 1
                    expression.pop(i)
            return expression
        self.tokens = separate([self.expression])

    def _validate_operators(self) -> None:
        """Raise an error if operators are not valid."""
        for operator in self.operators:
            if not isinstance(operator, str):
                raise InvalidOperatorException(
                    f"{operator} is not valid. has to be be an str.")
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

    def _validate_variables(self) -> None:
        """Raise an error if variables are not valid."""
        if not self.variables:
            return
        for variable in self.variables:
            if not isinstance(variable, str):
                raise TypeError(
                    f"variable has to be a str. {variable} is {type(variable)}, not str.")
            if len(variable) > 1:
                raise InvalidVariableException(f"{variable}'s has to be 1")

    def _validate_operators_associativity(self) -> None:
        """Raise an error if operators_associativity is not valid."""
        for operator in self.operators:
            if operator not in self.operators_associativity.keys():
                raise MissingOperatorsInfoException(
                    f"{operator}'s associativity is missing.")
            if self.operators_associativity[operator] != 'LR' and self.operators_associativity[operator] != 'RL':
                raise InvalidOperatorAssociativityException(
                    f"{operator}'s associativity is not valid")

    def _validate_parenthesis(self) -> None:
        """Raise an error if expression's parenthesis are not valid."""
        stack = []
        for c in self.tokens:
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

    def _validate_Expression(self, tokens: List[str]) -> None:
        """Raise an error if expression is not valid."""
        if not tokens:
            raise InvalidExpressionException(
                f"{self.expression} is not a valid expression.")
        sz = len(tokens)
        is_previous_character_operand = False
        i = 0
        while i < sz:
            if self._is_open_bracket(tokens[i]):
                if is_previous_character_operand:
                    raise InvalidExpressionException(
                        f"{self.expression} is not a valid expression.")
                open_brackets_count = 0
                idx = i

                # Find its close bracket
                while open_brackets_count != 1 or not self._is_close_bracket(tokens[idx]):
                    if self._is_open_bracket(tokens[idx]):
                        open_brackets_count += 1
                    if self._is_close_bracket(tokens[idx]):
                        open_brackets_count -= 1
                    idx += 1
                    if idx >= sz:
                        raise InvalidParenthesesException(
                            f"{self.expression}'s parenthesis are not balanced.")

                self._validate_Expression(tokens[i + 1: idx])

                i = idx
                is_previous_character_operand = True

            elif self._is_close_bracket(tokens[i]):
                raise InvalidParenthesesException(
                    f"{self.expression}'s parenthesis are not balanced.")

            elif self.is_operand(tokens[i]):
                if is_previous_character_operand:
                    raise InvalidExpressionException(
                        f"{self.expression} is not a valid expression.")
                is_previous_character_operand = True

            elif self.is_unary_operator(tokens[i]):
                if self.operators_associativity[tokens[i]] == 'LR':
                    if not is_previous_character_operand:
                        raise InvalidExpressionException(
                            f"{self.expression} is not valid")
                else:
                    if is_previous_character_operand:
                        raise InvalidExpressionException(
                            f"{self.expression} is not a valid expression.")

            elif self.is_binary_operator(tokens[i]):
                if not is_previous_character_operand:
                    raise InvalidExpressionException(
                        f"{self.expression} is not a valid expression.")
                is_previous_character_operand = False
            else:
                raise InvalidExpressionException(
                    f"{self.expression} is not a valid expression.")

            i += 1
        if not is_previous_character_operand:
            raise InvalidExpressionException(
                f"{self.expression} is not a valid expression.")

    def _validate(self) -> bool:
        """Return True if expression is valid."""
        self._validate_operators()
        self._validate_operators_associativity()
        self._validate_variables()
        self._validate_parenthesis()
        self._validate_Expression(self.tokens)

        return True

    def postfix(self) -> List[str]:
        """Return the postfix form for the expression."""
        postfix = []
        operators_stack = []
        for c in self.tokens:
            if self.is_operand(c):
                postfix.append(c)
            elif self.is_binary_operator(c) or self.is_unary_operator(c):
                while operators_stack and not self._is_open_bracket(operators_stack[-1]) and self._has_higher_precedence(operators_stack[-1], c):
                    postfix.append(operators_stack[-1])
                    operators_stack.pop()
                operators_stack.append(c)
            elif self._is_open_bracket(c):
                operators_stack.append(c)
            elif self._is_close_bracket(c):
                while not self._is_open_bracket(operators_stack[-1]):
                    postfix.append(operators_stack[-1])
                    operators_stack.pop()
                operators_stack.pop()
        while operators_stack:
            postfix.append(operators_stack[-1])
            operators_stack.pop()
        return postfix

    def prefix(self) -> str:
        """Return the prefix form for the expression."""
        temp_tokens = self.tokens
        self.tokens = self.tokens[::-1]

        for idx, c in enumerate(self.tokens):
            if c == "(":
                self.tokens[idx] = ")"
            elif c == ")":
                self.tokens[idx] = "("
            elif c == "{":
                self.tokens[idx] = "}"
            elif c == "}":
                self.tokens[idx] = "{"
            elif c == "[":
                self.tokens[idx] = "]"
            elif c == "]":
                self.tokens[idx] = "["
            else:
                self.tokens[idx] = c
        prefix = self.postfix()[::-1]
        self.tokens = temp_tokens
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
                if self.operators_associativity[c] == "LR":
                    node.left = stack.pop()
                else:
                    node.right = stack.pop()
            stack.append(node)
        return stack.pop()

    def update_operator_info(self, *, operator: str, operator_info: Tuple[int, int]) -> None:
        """Update the info of an operator."""
        self.operators_info[operator] = operator_info
        self.validate()

    def get_operands(self) -> set:
        """Return set that contains all symbols in the expression."""
        symbols = {symbol for symbol in self.tokens if self.is_operand(symbol)}
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
