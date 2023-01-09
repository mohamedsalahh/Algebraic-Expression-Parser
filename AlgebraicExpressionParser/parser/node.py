from typing import Any, List, Optional


class Node:
    def __init__(self, value: Any, *, left: Optional["Node"] = None, right: Optional["Node"] = None) -> None:
        self.value = value
        self.left = left
        self.right = right

    @property
    def left(self) -> "Node":
        return self._left

    @left.setter
    def left(self, left: "Node") -> None:
        if isinstance(left, Node) or left == None:
            self._left = left
        else:
            raise TypeError(
                f"{left}Node children has to be Node instances.")

    @property
    def right(self) -> "Node":
        return self._right

    @right.setter
    def right(self, right: "Node") -> None:
        if isinstance(right, Node) or right == None:
            self._right = right
        else:
            raise TypeError(
                f"Node children has to be Node instances.")

    def __str__(self) -> str:
        return f"Node: (value: {self.value}, left: {self.left}, right: {self.right})"

    def __repr__(self) -> str:
        return f"Node(value={self.value}, left={self.left}, right={self.right})"

    def _preorder(self, root: "Node", result: List) -> None:
        if not root:
            return
        result.append(root.value)
        self._preorder(root.left, result)
        self._preorder(root.right, result)

    def _inorder(self, root: "Node", result: List) -> None:
        if not root:
            return
        self._inorder(root.left, result)
        result.append(root.value)
        self._inorder(root.right, result)

    def _postorder(self, root: "Node", result: List) -> None:
        if not root:
            return
        self._postorder(root.left, result)
        self._postorder(root.right, result)
        result.append(root.value)

    def preorder(self) -> List["Node"]:
        result = []
        self._preorder(self, result)
        return result

    def inorder(self) -> List["Node"]:
        result = []
        self._inorder(self, result)
        return result

    def postorder(self) -> List["Node"]:
        result = []
        self._postorder(self, result)
        return result
