# 04 Message Queue & Async

> 状态：路线骨架。

目标：用崩溃实验理解消息为什么会丢、重、乱，以及 ACK、重试、DLQ 和幂等怎样组合。

## 计划顺序

1. `01-in_memory_queue.py`
2. `02-producer_broker_consumer.py`
3. `03-ack_and_crash.py`
4. `04-retry_and_dlq.py`
5. `05-idempotent_consumer.py`
6. `06-transactional_outbox.py`
7. `07-rabbitmq_visual.md`
8. `08-kafka_partition.py`
9. `09-kafka_ui_visual.md`
10. `90-saleor_mapping.md`

Visual Lab：RabbitMQ 官方 Management Plugin 观察 ready/unacked 和 rate；Kafbat UI 观察 Topic、Partition、Consumer Group 与 Lag。
