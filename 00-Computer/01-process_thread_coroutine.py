"""
01 - 进程、线程、协程：先看“谁隔离、谁共享、谁调度”。

现实问题
--------
Web 请求、数据库等待、图片压缩、Celery 任务都叫“任务”，但它们占用的
地址空间、线程和 CPU 并不相同。选模型前，先回答三个问题：

1. 状态是否与其他任务共享？
2. 谁决定何时切换？操作系统，还是代码中的 await？
3. 任务能否真的同时占用多个 CPU 核？

运行：python3 00-Computer/01-process_thread_coroutine.py
"""

from __future__ import annotations

import asyncio
import os
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass


@dataclass(frozen=True)
class Identity:
    label: str
    process_id: int
    thread_name: str


def current_identity(label: str) -> Identity:
    """线程共享 PID，但每个线程有自己的名字/栈。"""
    return Identity(label, os.getpid(), threading.current_thread().name)


def run_processes(labels: tuple[str, ...]) -> list[Identity]:
    """启动独立解释器；stdout 是最小的进程间通信通道。"""
    child_code = (
        "import os,sys,threading,time; "
        "time.sleep(0.05); "
        "print(sys.argv[1], os.getpid(), threading.current_thread().name, sep='\\t')"
    )
    children = [
        subprocess.Popen(
            [sys.executable, "-c", child_code, label],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for label in labels
    ]
    identities: list[Identity] = []
    for child in children:
        stdout, stderr = child.communicate()
        if child.returncode:
            raise RuntimeError(f"child process failed: {stderr.strip()}")
        label, process_id, thread_name = stdout.strip().split("\t")
        identities.append(Identity(label, int(process_id), thread_name))
    return identities


async def coroutine_job(label: str) -> Identity:
    # await 是协作切换点：当前 Task 暂停，事件循环可以运行别的 Task。
    await asyncio.sleep(0)
    return current_identity(label)


def run_threads(shared: list[str]) -> list[Identity]:
    def thread_job(label: str) -> Identity:
        shared.append(label)  # 两个线程能看见同一个 list
        return current_identity(label)

    with ThreadPoolExecutor(max_workers=2, thread_name_prefix="lesson-thread") as pool:
        return list(pool.map(thread_job, ("thread-A", "thread-B")))


async def run_coroutines() -> list[Identity]:
    return await asyncio.gather(
        coroutine_job("task-A"),
        coroutine_job("task-B"),
    )


def self_check() -> None:
    shared: list[str] = []
    threads = run_threads(shared)
    assert sorted(shared) == ["thread-A", "thread-B"]
    assert all(item.process_id == os.getpid() for item in threads)

    processes = run_processes(("process-A", "process-B"))
    assert len({item.process_id for item in processes}) == 2
    assert all(item.process_id != os.getpid() for item in processes)

    coroutines = asyncio.run(run_coroutines())
    assert len({item.process_id for item in coroutines}) == 1
    assert len({item.thread_name for item in coroutines}) == 1


def main() -> None:
    print(f"parent: pid={os.getpid()} thread={threading.current_thread().name}")

    shared: list[str] = []
    threads = run_threads(shared)
    print(f"threads: {threads}")
    print(f"thread-shared list visible in parent: {shared}")

    # 子进程有独立地址空间；这里把 stdout 当作最小 IPC，把结果传回父进程。
    processes = run_processes(("process-A", "process-B"))
    print(f"processes: {processes}")

    coroutines = asyncio.run(run_coroutines())
    print(f"coroutines: {coroutines}")
    print("observe: coroutine tasks share one process/thread until work is offloaded")


if __name__ == "__main__":
    self_check()
    main()


# 生产故障
# --------
# - threading.Lock 只保护一个进程；多 worker/多 Pod 不能靠本地锁防重复扣库存。
# - async def 内调用阻塞 SDK，会卡住同一事件循环上的其他请求。
# - 进程间传输大对象有序列化和复制成本，多进程不一定比单进程快。
#
# 面试追问
# --------
# 线程由操作系统抢占式调度并共享进程内存；协程通常在 await 处协作切换；
# 进程地址空间隔离，适合 CPU 并行和故障隔离，但 IPC 成本更高。
#
# 费曼问题
# --------
# 为什么在单机两个 Web worker 中使用一个全局 dict，两个请求可能看见不同状态？
