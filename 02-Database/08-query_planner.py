"""
08 - Query Planner toy cost：为什么有索引也可能 Seq Scan。

这个模型不是 PostgreSQL 真实公式，只保留选择性带来的成本交叉：
Seq cost   ≈ 全表页 + 全表行 CPU
Index cost ≈ 树高随机页 + 匹配页随机访问 + 匹配行 CPU

运行：python3 02-Database/08-query_planner.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Cost:
    seq_scan: float
    index_scan: float

    @property
    def chosen(self) -> str:
        return "Index Scan" if self.index_scan < self.seq_scan else "Seq Scan"


def estimate_cost(
    total_rows: int,
    selected_rows: int,
    *,
    rows_per_page: int = 100,
    index_height: int = 3,
    seq_page_cost: float = 1.0,
    random_page_cost: float = 4.0,
    row_cpu_cost: float = 0.01,
) -> Cost:
    if not 0 <= selected_rows <= total_rows:
        raise ValueError("selected_rows must be between zero and total_rows")
    table_pages = math.ceil(total_rows / rows_per_page)
    selected_pages = math.ceil(selected_rows / rows_per_page)
    seq = table_pages * seq_page_cost + total_rows * row_cpu_cost
    index = (
        index_height * random_page_cost
        + selected_pages * random_page_cost
        + selected_rows * row_cpu_cost
    )
    return Cost(seq, index)


def self_check() -> None:
    assert estimate_cost(100_000, 100).chosen == "Index Scan"
    assert estimate_cost(100_000, 90_000).chosen == "Seq Scan"


def main() -> None:
    for selected in (100, 90_000):
        cost = estimate_cost(100_000, selected)
        selectivity = selected / 100_000
        print(
            f"selected={selected:<6} selectivity={selectivity:>6.1%} "
            f"seq={cost.seq_scan:.1f} index={cost.index_scan:.1f} -> {cost.chosen}"
        )


if __name__ == "__main__":
    self_check()
    main()


# 诊断顺序
# --------
# 在 EXPLAIN ANALYZE 中先找 estimated rows 与 actual rows 最早分叉的节点，再看
# loops、Rows Removed by Filter、Buffers、Sort/Hash spill。估算错时检查统计信息、
# 数据倾斜和列相关性，不要第一反应就强制索引。
#
# 费曼问题
# --------
# 同一个 status 索引，为什么查询 0.1% 的 FAILED 和 99% 的 SUCCESS 可能用不同计划？
