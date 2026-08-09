# 12 - 事务与锁演化（后续制作骨架）

```text
单条写入
→ 多条写入中途失败
→ Transaction / ACID
→ 并发读写互相覆盖
→ Lock
→ 读多写少时锁竞争
→ MVCC
→ 多行锁顺序不一致
→ Deadlock detection / retry
→ 多服务事务边界断裂
→ Outbox / Saga
```

制作本节时必须回答：单用户程序为什么不需要先讲隔离级别；为什么不能给所有查询都加 `SELECT FOR UPDATE`；MVCC 降低了哪类冲突，又没有消除哪类写冲突。

Saleor 入口：`saleor/checkout/models.py:Checkout.safe_update`、`saleor/checkout/lock_objects.py`、checkout complete 调用链。当前只登记入口，完整实验留到事务批次。

Java/Spring 对应：`@Transactional` 只定义事务边界，隔离、行锁、死锁和重试仍由数据库与业务访问顺序共同决定。

费曼题：为什么 `transaction.atomic()` 能保证一起提交，却不能自动阻止两个请求都先读到旧库存？

## Sources

- [PostgreSQL: Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [PostgreSQL: Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html)
- [《凤凰架构》事务处理](https://icyfenix.cn/architect-perspective/general-architecture/transaction/)
