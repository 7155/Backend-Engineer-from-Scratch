"""
02 - Buffer Pool：五次逻辑读取为什么只做三次底层读取。

输入：缓存容量 2，访问页 0 → 1 → 0 → 2 → 0。
规则：命中时把页移到“最近使用”；未命中且已满时淘汰最久未使用页。

运行：python3 02-Database/02-buffer_pool.py
"""

from __future__ import annotations

import runpy
import tempfile
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path

PAGE = runpy.run_path(str(Path(__file__).with_name("01-page_io.py")))
DiskManager = PAGE["DiskManager"]


@dataclass(frozen=True)
class BufferStats:
    hits: int
    misses: int
    evictions: int


class BufferPool:
    """教学版 write-through Buffer Pool；OrderedDict 从 LRU 排到 MRU。"""

    def __init__(self, disk, capacity: int = 2) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.disk = disk
        self.capacity = capacity
        self._pages: OrderedDict[int, bytes] = OrderedDict()
        self._hits = self._misses = self._evictions = 0

    @property
    def cached_page_ids(self) -> tuple[int, ...]:
        return tuple(self._pages)

    @property
    def stats(self) -> BufferStats:
        return BufferStats(self._hits, self._misses, self._evictions)

    def get_page(self, page_id: int) -> bytes:
        if page_id in self._pages:
            self._hits += 1
            self._pages.move_to_end(page_id)
            return self._pages[page_id]

        self._misses += 1
        page = self.disk.read_page(page_id)
        if len(self._pages) >= self.capacity:
            self._pages.popitem(last=False)
            self._evictions += 1
        self._pages[page_id] = page
        return page


def build_demo():
    directory = tempfile.TemporaryDirectory()
    disk = DiskManager(Path(directory.name) / "tiny.db", page_size=32)
    for value in (b"orders-page", b"users-page", b"stocks-page"):
        disk.allocate_page(value)
    return directory, disk, BufferPool(disk, capacity=2)


def self_check() -> None:
    directory, disk, pool = build_demo()
    try:
        for page_id in (0, 1, 0, 2, 0):
            pool.get_page(page_id)
        assert pool.cached_page_ids == (2, 0)
        assert pool.stats == BufferStats(hits=2, misses=3, evictions=1)
        assert disk.read_count == 3
    finally:
        directory.cleanup()


def main() -> None:
    directory, disk, pool = build_demo()
    try:
        for page_id in (0, 1, 0, 2, 0):
            value = pool.get_page(page_id).rstrip(bytes([0])).decode()
            print(f"read={page_id} value={value:<11} cache={pool.cached_page_ids}")
        print(f"stats={pool.stats} physical_file_reads={disk.read_count}")
    finally:
        directory.cleanup()


if __name__ == "__main__":
    self_check()
    main()


# 生产差距
# --------
# 真实 Buffer Pool 还要处理：dirty page、pin/unpin、并发 latch、WAL 先写、
# checkpoint、预读和抗顺序扫描污染。LRU 只是理解替换的最小模型。
#
# 故障观察
# --------
# 工作集大于缓存时会反复淘汰，形成 cache thrashing；要同时看 buffer hit/read、
# 查询计划、表/索引大小和底层 I/O，单一“命中率很高”不等于请求健康。
