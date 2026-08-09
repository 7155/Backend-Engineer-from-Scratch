# 03 - 从单应用思维到多 Pod 运行模型

## V0：一个应用实例

一个实例足够承载负载时，本地内存 cache、进程内锁和后台线程都很诱人：实现短、延迟低、调试直观。

## 演化链

```text
单实例
→ 容量或可用性超过单机边界
→ 多 Web 进程 / Pod + Load Balancer
→ 下一次请求不保证落到同一进程
→ 共享 PostgreSQL / Redis / Broker
→ 并发执行与重复投递
→ 原子更新、行锁、幂等
→ Worker 可能早于事务提交读数据
→ transaction.on_commit
→ Pod 被终止
→ bounded retry + graceful shutdown + observability
```

## 当前源码证据

- `AGENTS.md` 明确说明多个 Web/Celery Pod 共享 PostgreSQL/read replicas 与 Redis/broker。
- 同一文件禁止把本地状态当真相，并要求任务可重试且幂等。
- `saleor/checkout/models.py:Checkout.safe_update` 使用 `transaction.atomic()` 与 `select_for_update()`。
- `saleor/checkout/lock_objects.py` 按主键排序后创建 checkout/line 行锁 QuerySet，降低锁顺序不一致风险。

## 不能过度推断

历史 commit 存在 Dockerfile/docker-compose 和 Celery 依赖，不等于所有 2017 生产部署都只有一个实例。这里的“单应用”是学习用 V0，不是对当年真实集群规模的断言。

## 为什么多 Pod 不免费

- 本地 session、锁、缓存和任务队列不再可靠。
- 每个 Pod/Worker 都会消耗数据库连接。
- 超时重试可能放大负载并重复写入。
- 发布与终止必须处理在途请求和任务。

## Java/Spring 对应

多副本 Spring Boot 也不能用 `synchronized` 或本地 `ConcurrentHashMap` 保护跨 Pod 业务不变量；需要数据库约束/锁、共享存储和幂等 key。

## 费曼复述

为什么 `transaction.on_commit` 只解决“任务早于提交”，仍没有解决 Broker 重投造成的重复执行？
