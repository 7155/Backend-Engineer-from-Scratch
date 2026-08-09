# 04 - 并发模型为什么不断演化

## V0：一个进程顺序处理

个人工具或管理脚本一次只做一件事，顺序执行最容易验证，也没有共享状态竞争。此时引入线程池和事件循环只会增加调试成本。

```text
request A：CPU 2 ms + DB 等待 50 ms
request B：必须等 A 完成
```

当并发为 1，这完全合理；当 100 个请求都在等数据库，CPU 大部分时间空闲，队列延迟才成为触发信号。

## 演化链

| 版本 | 解决办法 | 解决的问题 | 新问题 |
| --- | --- | --- | --- |
| V0 | 单进程顺序执行 | 实现和状态最简单 | 一个慢任务阻塞后续任务 |
| V1 | 每个请求一个线程 | I/O 等待可以重叠 | 线程栈、切换和共享内存竞争 |
| V2 | 固定线程池 | 限制线程数量 | 队列仍可能无限增长 |
| V3 | Event Loop + coroutine | 用少量线程承载大量 I/O 等待 | 一次阻塞调用会卡住整条 loop |
| V4 | 多进程/多 Pod + 后台 Worker | CPU 并行、故障隔离、水平扩展 | 本地状态失效、重复执行、跨进程协调 |

## 一个具体输入

运行 `02-cpu_bound_vs_io_bound.py`。四个 80 ms 的等待可以通过线程或 coroutine 重叠；四个很短的 CPU 任务却可能因进程启动成本而更慢。这说明升级条件是工作负载，不是“异步更先进”。

## 为什么不是一开始就多 Pod

- 单实例没有跨节点网络失败和重复投递。
- 本地调试、事务定位和部署都更简单。
- 流量尚未超过单实例容量时，多 Pod 不减少单次业务计算。
- 多实例会立刻要求共享状态、幂等、分布式可观测性和安全停机。

## Saleor 位于哪一层

Saleor `3.23.25` 的 `AGENTS.md` 明确描述多 Kubernetes Pod、Web/Celery Worker、共享 PostgreSQL 与 Redis/broker。它处于 V4，因此要求：不把本地内存作为真相、任务可重试且幂等、事务提交后再调度后台任务。

这是当前源码约束；“哪些历史事故推动了这些规则”仍是推断，不能只凭当前文档断言。

## Java/Spring 对应

- Thread：Servlet worker thread、`ExecutorService`。
- Coroutine/Event Loop：Reactor、Spring WebFlux。
- 后台 Worker：`@Async` 只是进程内执行；RabbitMQ/Kafka consumer 才跨进程持久协调。
- 多实例：Spring Boot 多 Pod 同样不能依赖本地 `Map` 防重复写入。

## 费曼复述

为什么把同步 Web 服务改成 async，可能提高 I/O 并发，却完全没有提高数据库连接池上限？

## Sources

- [Python `threading`](https://docs.python.org/3/library/threading.html)
- [Python `multiprocessing`](https://docs.python.org/3/library/multiprocessing.html)
- [Python `asyncio`](https://docs.python.org/3/library/asyncio.html)
