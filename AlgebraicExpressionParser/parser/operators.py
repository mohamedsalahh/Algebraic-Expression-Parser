import copy
from typing import List, Optional, Set, Union


class Operator:
    """Operator rules holder"""

    prefix = "prefix"
    infix = "infix"
    postfix = "postfix"
    unary = 1
    binary = 2
    ltr = "LR"
    rtl = "RL"

    def __init__(self, *, symbol: str, type: Optional["int"] = binary, precedence: Optional["int"] = 1, associativity: Optional["str"] = ltr, position: Optional["str"] = infix) -> None:
        """
        symbol: represents the operator.
            type: str
        type: represents the operator type. It accepts two values unary or binary.
            type: str
            default: binary
        precedence: represents the operator precedence.
            type: int
            default: 1
        associativity: represents the operator associativity. It accept two values ltr for left-to-right or rtl right-to-left.
            type: str
            default: ltr
        position: string represents the operator position. It accept three values prefix, infix or postfix.
            type: str
            default: infix
        """
        self.symbol = symbol
        self.type = type
        self.precedence = precedence
        self.associativity = associativity
        self.position = position

    @property
    def symbol(self) -> str:
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: str) -> None:
        if not isinstance(symbol, str):
            raise TypeError(
                f"Invalid operator symbol. It has to be str.")
        self._symbol = symbol

    @property
    def type(self) -> int:
        return self._type

    @type.setter
    def type(self, type: int) -> None:
        if not type in [self.unary, self.binary]:
            raise TypeError(
                f"Invalid operator type.")
        self._type = type

    @property
    def precedence(self) -> int:
        return self._precedence

    @precedence.setter
    def precedence(self, precedence: int) -> None:
        if not isinstance(precedence, int):
            raise TypeError(
                f"Invalid operator precedence. It has to be int.")
        self._precedence = precedence

    @property
    def associativity(self) -> str:
        return self._associativity

    @associativity.setter
    def associativity(self, associativity: str) -> None:
        if not associativity in [self.ltr, self.rtl]:
            raise TypeError(
                f"Invalid operator associativity.")
        self._associativity = associativity

    @property
    def position(self) -> str:
        return self._position

    @position.setter
    def position(self, position: str) -> None:
        if not position in [self.prefix, self.infix, self.postfix]:
            raise TypeError(
                f"Invalid operator position.")
        self._position = position

    def __str__(self) -> str:
        return f"symbol: {self.symbol}\ntype: {self.type}\nprecedence: {self.precedence}\nassociativity: {self.associativity}\nposition: {self.position}"

    def __repr__(self) -> str:
        return f"Operator(symbol='{self.symbol}', type={self.type}, precedence={self.precedence}, associativity='{self.associativity}')"


class Operators:
    """Operators holder"""

    def __init__(self, operators: Union[List[Operator], Set[Operator]]) -> None:
        """
        operators: list of Operator instances that holds operators symbols and rules.
            type: list or set
        """
        self.operators = operators

    @property
    def operators(self) -> List[Operator]:
        return self._operators

    @operators.setter
    def operators(self, operators: Union[List[Operator], Set[Operator]]) -> None:
        if not isinstance(operators, (list, set)):
            raise TypeError(
                f"operators has to be list. {operators} is {type(operators)}.")
        self._operators = set(copy.copy(operators))
        self._validate()

    def __str__(self) -> str:
        return f"operators: {self.operators}"

    def __repr__(self) -> str:
        return f"Operators({self.operators})"

    def _validate(self) -> bool:
        for operator in self.operators:
            if not isinstance(operator, Operator):
                raise TypeError(
                    f"operators has to be list of Operator instances. {operator} is {type(operator)}.")
        return True

    def add_operator(self, operator: Operator) -> None:
        if not isinstance(operator, Operator):
            raise TypeError(
                f"operator has to be Operator instance. {operator} is {type(operator)}.")
        self.operators.add(operator)

    def get_operators(self) -> Set[Operator]:
        """Return set that contains all operators."""
        return {operator for operator in self.operators}

    def get_operators_symbol(self) -> Set[str]:
        """Return set that contains all operators symbols."""
        return {operator.symbol for operator in self.operators}

    def get_binary_operators_symbols(self) -> Set[str]:
        """Return set that contains all binary operators symbols."""
        return {operator.symbol for operator in self.operators if operator.type == Operator.binary}

    def get_binary_operators(self) -> Set[Operator]:
        """Return set that contains all binary operators."""
        return {operator for operator in self.operators if operator.type == Operator.binary}

    def get_unary_operators_symbols(self) -> Set[str]:
        """Return set that contains all unary operators symbols."""
        return {operator.symbol for operator in self.operators if operator.type == Operator.unary}

    def get_unary_operators(self) -> Set[Operator]:
        """Return set that contains all unary operators."""
        return {operator for operator in self.operators if operator.type == Operator.unary}
    
    def is_operator(self, c: str) -> bool:
        return c in self.get_operators_symbol()

    def is_binary_operator(self, c: str) -> bool:
        return c in self.get_binary_operators_symbols()

    def is_unary_operator(self, c: str) -> bool:
        return c in self.get_unary_operators_symbols()

    def get_operator_rules(self, c: str) -> Set[Operator]:
        """Return all operator rules. There are Some operator has many rules, like '-', it may be minus or negative."""
        return {operator for operator in self.operators if operator.symbol == c}

    def does_have_higher_precedence(self, operator1: Operator, operator2: Operator) -> bool:
        # if operator1.precedence == operator2.precedence:
        #     return operator1.associativity == Operator.ltr
        # return operator1.precedence > operator2.precedence
        return (operator2.associativity == Operator.ltr and operator2.precedence <= operator1.precedence) or (operator2.associativity == Operator.rtl and operator2.precedence < operator1.precedence)
    
