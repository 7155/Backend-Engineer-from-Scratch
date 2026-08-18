"""
02 - CPU-bound 与 I/O-bound：不要背“线程快/协程快”，先看时间花在哪里。

具体输入
--------
- 四个纯 Python 平方和：主要占 CPU。
- 四个各等待 0.08 秒的任务：主要等待网络/数据库。

预期趋势
--------
- 顺序 I/O 约 4 × 0.08 秒；线程和协程把等待重叠，接近 0.08 秒。
- CPU 计时没有固定赢家：核心数、任务大小、进程启动和系统负载都会改变结果。

运行：python3 00-Computer/02-cpu_bound_vs_io_bound.py
"""

from __future__ import annotations

import asyncio
import subprocess
import sys
import time
from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass


@dataclass(frozen=True)
class Timing:
    model: str
    seconds: float
    completed: int


def cpu_work(limit: int) -> int:
    # CPython 同一解释器中的线程执行纯 Python 字节码会受 GIL 约束。
    return sum(number * number for number in range(limit))


def blocking_io(delay: float) -> int:
    time.sleep(delay)  # 模拟阻塞 socket/数据库调用
    return 1


async def async_io(delay: float) -> int:
    await asyncio.sleep(delay)  # 等待时把控制权交回事件循环
    return 1


def measure(model: str, call: Callable[[], Iterable[int]]) -> Timing:
    started = time.perf_counter()
    results = tuple(call())
    return Timing(model, time.perf_counter() - started, len(results))


def run_cpu_processes(limits: tuple[int, ...]) -> tuple[int, ...]:
    """并发启动独立 Python 进程，绕过同一解释器的 GIL。"""
    children = [
        subprocess.Popen(
            [sys.executable, __file__, "--cpu-child", str(limit)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for limit in limits
    ]
    results: list[int] = []
    for child in children:
        stdout, stderr = child.communicate()
        if child.returncode:
            raise RuntimeError(f"CPU child failed: {stderr.strip()}")
        results.append(int(stdout.strip()))
    return tuple(results)


def compare_cpu(limits: tuple[int, ...]) -> list[Timing]:
    sequential = measure("sequential", lambda: map(cpu_work, limits))

    def threads() -> tuple[int, ...]:
        with ThreadPoolExecutor(max_workers=len(limits)) as pool:
            return tuple(pool.map(cpu_work, limits))

    def processes() -> tuple[int, ...]:
        return run_cpu_processes(limits)

    return [sequential, measure("threads", threads), measure("processes", processes)]


def compare_blocking_io(delays: tuple[float, ...]) -> list[Timing]:
    sequential = measure("sequential", lambda: map(blocking_io, delays))

    def threads() -> tuple[int, ...]:
        with ThreadPoolExecutor(max_workers=len(delays)) as pool:
            return tuple(pool.map(blocking_io, delays))

    return [sequential, measure("threads", threads)]


async def compare_async_io(delays: tuple[float, ...]) -> Timing:
    started = time.perf_counter()
    results = await asyncio.gather(*(async_io(delay) for delay in delays))
    return Timing("asyncio", time.perf_counter() - started, len(results))


def self_check() -> None:
    assert cpu_work(5) == 30
    delays = (0.005, 0.005, 0.005)
    sequential, threads = compare_blocking_io(delays)
    assert sequential.completed == threads.completed == 3
    assert threads.seconds < sequential.seconds
    assert asyncio.run(compare_async_io((0.001, 0.001))).completed == 2


def show(title: str, timings: list[Timing]) -> None:
    print(title)
    for item in timings:
        print(f"  {item.model:<10} {item.seconds:.3f}s completed={item.completed}")


def main() -> None:
    limits = (350_000,) * 4
    delays = (0.08,) * 4
    show("CPU-bound (machine-dependent)", compare_cpu(limits))
    show(
        "I/O-bound",
        compare_blocking_io(delays) + [asyncio.run(compare_async_io(delays))],
    )
    print("conclusion: choose by workload and resource boundary, not one timing")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--cpu-child":
        print(cpu_work(int(sys.argv[2])))
    else:
        self_check()
        main()


# 生产故障
# --------
# 创建十万个协程不会创造十万个数据库连接。真正上限仍是连接池、下游 QPS、
# 内存和 CPU；必须用 semaphore、超时和背压限制并发。
#
# 练习提示
# --------
# “有 GIL 就不能用线程”是错的：I/O 等待会给其他线程执行机会；很多原生扩展
# 也会释放 GIL。纯 Python CPU 计算若需要多核，通常用多进程或进程外 worker。
#
# 费曼问题
# --------
# 为什么四个 0.08 秒的等待可以接近 0.08 秒完成，却不代表 CPU 做快了四倍？