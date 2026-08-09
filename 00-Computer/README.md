# 00 Computer Foundations

目标：能解释为什么 Web Server、Worker、数据库连接和长任务都受并发模型约束。

## 学习顺序

1. `01-process_thread_coroutine.py`：先看隔离、共享和调度单位。
2. `02-cpu_bound_vs_io_bound.py`：再用计时区分计算与等待。
3. `03-event_loop_visual.html`：离线逐步观察 `await` 如何让出执行权，以及 CPU 长任务怎样阻塞事件循环。
4. `04-concurrency_evolution.md`：顺序执行怎样演化到线程、协程、Worker 和多 Pod。
5. `90-saleor_mapping.md`：最后区分 Saleor 在线 API 与 Celery worker 的运行入口。

运行：

```bash
python3 00-Computer/01-process_thread_coroutine.py
python3 00-Computer/02-cpu_bound_vs_io_bound.py
open 00-Computer/03-event_loop_visual.html
```

## 国内面试关键词

进程/线程/协程、GIL、并发与并行、CPU-bound/I/O-bound、事件循环阻塞、请求线程长任务、连接池上限。

## 费曼复述

> 100 个请求都在等数据库，另有 4 个报表持续计算 2 秒。请解释你会把它们分别放在哪里，选错后用户会看到什么，并给出两个验证指标。
