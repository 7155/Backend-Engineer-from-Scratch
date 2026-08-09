"""
03 - 从普通二叉树到高扇出树：数据库真正想减少的是 Page 层数。

有序插入 1..32 会让未平衡 BST 退化成高度 32。若一个数据库节点能容纳 200 个
分支，一百万条记录的叶页导航层数可以非常浅。比较次数不是唯一成本；冷缓存下
每下降一层都可能是一次随机 Page I/O。

运行：python3 02-Database/03-btree.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class BinaryNode:
    key: int
    left: BinaryNode | None = None
    right: BinaryNode | None = None


class BinarySearchTree:
    def __init__(self) -> None:
        self.root: BinaryNode | None = None

    def insert(self, key: int) -> None:
        if self.root is None:
            self.root = BinaryNode(key)
            return
        node = self.root
        while True:
            if key < node.key:
                if node.left is None:
                    node.left = BinaryNode(key)
                    return
                node = node.left
            elif key > node.key:
                if node.right is None:
                    node.right = BinaryNode(key)
                    return
                node = node.right
            else:
                return

    @property
    def height(self) -> int:
        def visit(node: BinaryNode | None) -> int:
            return 0 if node is None else 1 + max(visit(node.left), visit(node.right))

        return visit(self.root)


def estimate_multiway_height(record_count: int, leaf_capacity: int, fanout: int) -> int:
    """叶子算一层；向上每层最多把 fanout 个 child 归到一个 parent。"""
    if record_count <= 0:
        return 0
    if leaf_capacity <= 0 or fanout < 2:
        raise ValueError("invalid capacity/fanout")
    nodes = math.ceil(record_count / leaf_capacity)
    height = 1
    while nodes > 1:
        nodes = math.ceil(nodes / fanout)
        height += 1
    return height


def self_check() -> None:
    tree = BinarySearchTree()
    for key in range(1, 11):
        tree.insert(key)
    assert tree.height == 10
    assert estimate_multiway_height(1_000_000, 200, 200) == 3


def main() -> None:
    tree = BinarySearchTree()
    for key in range(1, 33):
        tree.insert(key)
    print(f"sorted inserts -> ordinary BST height={tree.height}")
    print(
        "1,000,000 rows, leaf_capacity=200, fanout=200 "
        f"-> estimated height={estimate_multiway_height(1_000_000, 200, 200)}"
    )


if __name__ == "__main__":
    self_check()
    main()


# 从 B-Tree 过渡到 B+Tree
# ----------------------
# B-Tree 的内部节点也可存完整数据；B+Tree 把完整索引项集中在叶子，让内部节点
# 主要装 key + child pointer，从而提高扇出。下一文件会再加入叶子链表，让范围查询
# 只定位一次起点。
#
# 费曼问题
# --------
# 为什么“一个节点能装更多 key”会减少磁盘 I/O，而不只是减少 Python 比较次数？
