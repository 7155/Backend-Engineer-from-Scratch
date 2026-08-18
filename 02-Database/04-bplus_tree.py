"""
04 - 手写简化 B+Tree：insert / search / split / leaf link / range scan。

order=4 表示内部节点最多 4 个 children、3 个 keys。插入第 4 个 key 会溢出：
- 叶子分裂：完整 key/value 留在叶子，把右叶首 key“复制”到父节点作 separator。
- 内部分裂：中间 separator“上移”到父节点，不留在左右内部节点。
- 根分裂：创建新根，树高增加 1。

运行：python3 02-Database/04-bplus_tree.py
"""

from __future__ import annotations

from bisect import bisect_left, bisect_right
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Node:
    leaf: bool
    keys: list[int] = field(default_factory=list)
    parent: Node | None = None
    values: list[Any] = field(default_factory=list)
    children: list[Node] = field(default_factory=list)
    next_leaf: Node | None = None


class BPlusTree:
    """教学用内存 B+Tree；故意不实现 deletion。"""

    def __init__(self, order: int = 4) -> None:
        if order < 3:
            raise ValueError("order must be at least 3")
        self.order = order
        self.max_keys = order - 1
        self.root = Node(leaf=True)

    def _find_leaf(self, key: int) -> Node:
        node = self.root
        while not node.leaf:
            # separator k 的右子树负责 >= k，所以使用 bisect_right。
            node = node.children[bisect_right(node.keys, key)]
        return node

    def search(self, key: int) -> Any | None:
        leaf = self._find_leaf(key)
        index = bisect_left(leaf.keys, key)
        if index < len(leaf.keys) and leaf.keys[index] == key:
            return leaf.values[index]
        return None

    def insert(self, key: int, value: Any) -> None:
        leaf = self._find_leaf(key)
        index = bisect_left(leaf.keys, key)
        if index < len(leaf.keys) and leaf.keys[index] == key:
            leaf.values[index] = value
            return
        leaf.keys.insert(index, key)
        leaf.values.insert(index, value)
        if len(leaf.keys) > self.max_keys:
            self._split_leaf(leaf)

    def _split_leaf(self, leaf: Node) -> None:
        split_at = (len(leaf.keys) + 1) // 2
        right = Node(
            leaf=True,
            keys=leaf.keys[split_at:],
            values=leaf.values[split_at:],
            parent=leaf.parent,
            next_leaf=leaf.next_leaf,
        )
        leaf.keys = leaf.keys[:split_at]
        leaf.values = leaf.values[:split_at]
        leaf.next_leaf = right
        self._insert_in_parent(leaf, right.keys[0], right)

    def _insert_in_parent(self, left: Node, separator: int, right: Node) -> None:
        if left is self.root:
            self.root = Node(leaf=False, keys=[separator], children=[left, right])
            left.parent = self.root
            right.parent = self.root
            return

        parent = left.parent
        if parent is None:
            raise AssertionError("non-root node must have a parent")
        left_index = parent.children.index(left)
        parent.keys.insert(left_index, separator)
        parent.children.insert(left_index + 1, right)
        right.parent = parent
        if len(parent.keys) > self.max_keys:
            self._split_internal(parent)

    def _split_internal(self, node: Node) -> None:
        middle = len(node.keys) // 2
        promoted = node.keys[middle]
        right = Node(
            leaf=False,
            keys=node.keys[middle + 1 :],
            children=node.children[middle + 1 :],
            parent=node.parent,
        )
        node.keys = node.keys[:middle]
        node.children = node.children[: middle + 1]
        for child in right.children:
            child.parent = right
        self._insert_in_parent(node, promoted, right)

    def range_search(self, start: int, end: int) -> list[tuple[int, Any]]:
        if start > end:
            return []
        leaf = self._find_leaf(start)  # 只从根定位一次
        result: list[tuple[int, Any]] = []
        while leaf is not None:
            for key, value in zip(leaf.keys, leaf.values, strict=True):
                if key < start:
                    continue
                if key > end:
                    return result
                result.append((key, value))
            leaf = leaf.next_leaf  # 后续沿叶子链表扫描
        return result

    def render(self) -> str:
        lines: list[str] = []
        level = [self.root]
        while level:
            lines.append(" | ".join(f"{'L' if node.leaf else 'I'}{node.keys}" for node in level))
            level = [child for node in level if not node.leaf for child in node.children]
        return "\n".join(lines)

    def validate(self) -> None:
        """验证结构不变量；仅测试 search 返回值不足以发现断链。"""
        leaf_depths: set[int] = set()
        leaves_in_tree: list[Node] = []

        def first_key(node: Node) -> int:
            while not node.leaf:
                node = node.children[0]
            return node.keys[0]

        def visit(node: Node, depth: int) -> None:
            assert node.keys == sorted(node.keys)
            assert len(node.keys) <= self.max_keys
            if node.leaf:
                assert len(node.keys) == len(node.values)
                assert not node.children
                leaf_depths.add(depth)
                leaves_in_tree.append(node)
                return
            assert not node.values
            assert len(node.children) == len(node.keys) + 1
            for child in node.children:
                assert child.parent is node
                visit(child, depth + 1)
            for index, separator in enumerate(node.keys):
                assert separator == first_key(node.children[index + 1])

        visit(self.root, 0)
        assert len(leaf_depths) == 1
        linked: list[Node] = []
        leaf = leaves_in_tree[0]
        while leaf is not None:
            linked.append(leaf)
            leaf = leaf.next_leaf
        assert linked == leaves_in_tree


def self_check() -> None:
    import random

    keys = list(range(1, 51))
    random.Random(7).shuffle(keys)
    tree = BPlusTree(order=4)
    for key in keys:
        tree.insert(key, key * 10)
    tree.validate()
    assert [tree.search(key) for key in range(1, 51)] == [key * 10 for key in range(1, 51)]
    assert tree.range_search(7, 12) == [(key, key * 10) for key in range(7, 13)]


def main() -> None:
    tree = BPlusTree(order=4)
    for key in (10, 20, 5, 6, 12, 30, 7, 17):
        tree.insert(key, f"value-{key}")
    tree.validate()
    print(tree.render())
    print(f"search 12 -> {tree.search(12)}")
    print(f"range [6, 17] -> {tree.range_search(6, 17)}")


if __name__ == "__main__":
    self_check()
    main()


# 生产差距
# --------
# 删除/合并、重复 key、固定磁盘 Page、Buffer Pool、WAL、MVCC、并发 latch、
# vacuum 和崩溃恢复都未实现。一次 split 会修改多个页，生产数据库必须保证崩溃后
# 结构仍可恢复；不要把这个类移植进 Saleor。
#
# 练习题
# --------
# 为什么叶子分裂是“复制右叶首 key 到父节点”，内部节点分裂却是“把中间 key 上移”？