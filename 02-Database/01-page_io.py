"""
01 - Page I/O：数据库为什么不是“把所有行放进 Python List”。

现实问题
--------
持久数据在文件/块设备上。数据库通常按固定大小 Page 搬运，而不是逐行随机读取。
固定页让 page_id 可以直接映射为文件 offset，也给缓存、空间管理和 WAL 一个稳定单位。

本实验用 32 字节页；真实 PostgreSQL Page 的布局还包含 Header、item pointer、
tuple 和空闲空间。这里的 file.read 次数也不等于 SSD 真正读取次数，OS page cache
可能已经命中。

运行：python3 02-Database/01-page_io.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path


class PageError(ValueError):
    pass


class DiskManager:
    def __init__(self, path: Path, page_size: int = 32) -> None:
        if page_size <= 0:
            raise ValueError("page_size must be positive")
        self.path = path
        self.page_size = page_size
        self.read_count = 0
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)

    @property
    def page_count(self) -> int:
        size = self.path.stat().st_size
        if size % self.page_size:
            raise PageError("database file is not page aligned")
        return size // self.page_size

    def allocate_page(self, payload: bytes = b"") -> int:
        page_id = self.page_count
        self.write_page(page_id, payload, allow_append=True)
        return page_id

    def write_page(self, page_id: int, payload: bytes, *, allow_append: bool = False) -> None:
        if len(payload) > self.page_size:
            raise PageError(f"payload exceeds {self.page_size}-byte page")
        if page_id < 0 or page_id > self.page_count:
            raise PageError(f"invalid page id: {page_id}")
        if page_id == self.page_count and not allow_append:
            raise PageError("write would create an unallocated page")

        # 每个 page 固定大小；短 payload 用 0 补齐，页号可以 O(1) 计算偏移。
        page = payload.ljust(self.page_size, b"\x00")
        with self.path.open("r+b") as file:
            file.seek(page_id * self.page_size)
            file.write(page)

    def read_page(self, page_id: int) -> bytes:
        if not 0 <= page_id < self.page_count:
            raise PageError(f"invalid page id: {page_id}")
        with self.path.open("rb") as file:
            file.seek(page_id * self.page_size)
            page = file.read(self.page_size)
        self.read_count += 1
        return page


def self_check() -> None:
    with tempfile.TemporaryDirectory() as directory:
        disk = DiskManager(Path(directory) / "tiny.db", page_size=16)
        page_id = disk.allocate_page(b"order-42")
        page = disk.read_page(page_id)
        assert page_id == 0
        assert len(page) == 16
        assert page.rstrip(b"\x00") == b"order-42"
        try:
            disk.allocate_page(b"x" * 17)
        except PageError:
            pass
        else:
            raise AssertionError("oversized page must fail")


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        disk = DiskManager(Path(directory) / "tiny.db", page_size=32)
        for payload in (b"orders", b"users", b"stocks"):
            page_id = disk.allocate_page(payload)
            print(f"allocated page={page_id} offset={page_id * disk.page_size}")
        page = disk.read_page(1)
        print(f"read page=1 bytes={len(page)} value={page.rstrip(bytes([0])).decode()}")


if __name__ == "__main__":
    self_check()
    main()


# 生产故障
# --------
# - 一行可能跨页或把大字段放到溢出区域；“一行一页”是错的。
# - 页写到一半崩溃会损坏结构，生产数据库需要 WAL、校验和恢复协议。
# - 顺序和随机 Page I/O 的延迟常数差异很大，大 O 不能代替测量。
#
# 面试问题
# --------
# page_id → offset 是 O(1)，但一次 miss 仍要搬运 page_size 字节。数据库按页组织
# 是为了匹配块访问、利用局部性，并让缓存和恢复拥有稳定单位。
