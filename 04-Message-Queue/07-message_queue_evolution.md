# 07 - MQ 演化：后台线程为什么最终变成 Broker

```text
V0 请求内同步发邮件
→ 下游慢，请求也慢
→ V1 后台线程
→ 进程崩溃，任务丢失
→ V2 内存 Queue
→ 多实例各有自己的 Queue
→ V3 独立 Broker
→ Consumer 中途崩溃
→ ACK / redelivery
→ 重复消费
→ 幂等
→ 永久失败
→ Retry + DLQ
→ DB commit 但消息未发送
→ Transactional Outbox
```

## 为什么同步调用曾经合理

调用链短、下游稳定时，同步调用有最直观的成功/失败结果，不需要 Broker、Consumer、监控和补偿。后台线程只适合“任务丢失可以接受”的进程内优化。

## 优化成本

- Broker 解耦时间和实例，也把一次函数调用变成多个可独立失败的状态。
- ACK 防止无声丢失，但 redelivery 产生至少一次语义和重复执行。
- 幂等防重复副作用，却需要业务 key、持久记录和并发保护。
- DLQ 保存永久失败消息，却要求告警、重放权限和人工处置。
- Outbox 缩小 DB/消息双写窗口，却增加表、Relay、清理和投递延迟。

## RabbitMQ/Kafka 与 Spring

RabbitMQ 强调 queue/routing/ACK；Kafka 强调 log/partition/offset。Spring AMQP、Spring Kafka 和 Celery 只是客户端抽象，无法取消至少一次投递带来的业务幂等要求。

Saleor `3.23.25` 使用 Celery，并明确要求 transaction `on_commit` 后调度、任务幂等可重试。这说明它处于 Broker + retry-safe consumer 层；是否使用某种 Outbox 必须按具体事件路径验证。

## 为什么不是所有调用都发 MQ

用户必须立即得到结果、强一致读依赖刚写入数据、任务量很小或故障恢复不值得额外运维时，同步调用更清楚。

费曼题：ACK 解决了 Consumer 崩溃后的丢失，为什么它同时迫使业务设计幂等？

## Sources

- [RabbitMQ Reliability Guide](https://www.rabbitmq.com/docs/reliability)
- [Celery Tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
