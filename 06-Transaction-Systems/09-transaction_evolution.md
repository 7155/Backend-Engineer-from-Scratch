# 09 - 交易系统演化：从一条订单记录到补偿工作流

```text
V0 直接写订单
→ 库存与支付不是同一步
→ V1 本地数据库事务
→ 外部支付不受本地事务控制
→ V2 状态机 + 幂等回调
→ 支付结果未知
→ 查询/对账/超时终态
→ 跨服务部分成功
→ Saga compensation
→ 事件双写窗口
→ Transactional Outbox
```

## 为什么直接写订单曾经合理

无在线支付、单仓库、低并发的内部系统可以用一条记录表达交易；此时状态机和补偿只会让简单流程难读。

## 新方案的新问题

- 状态机限制非法跳转，也带来版本迁移和终态设计。
- 库存锁防超卖，却降低并发并可能死锁。
- 幂等回调防重复扣款，却需要稳定业务 key 和唯一约束。
- Saga 不提供瞬时强一致，补偿本身也可能失败。
- Outbox 保证事件最终可见，却不是“只发送一次”。

Saleor 映射入口：checkout create/complete、warehouse allocation、Payment/Transaction、Webhook。完整章必须按固定 commit 追事务、锁、任务和测试，不能把目录名当行为证据。Spring 对应 `@Transactional`、状态机、唯一约束、Outbox Relay 与 Saga orchestrator。

## 为什么不把所有步骤放一个长事务

外部支付无法加入 PostgreSQL 本地事务；长锁会占连接、阻塞库存并放大故障范围。

费曼题：支付请求超时后，为什么订单不能立刻标记“支付失败”，也不能盲目再次扣款？

## Sources

- [《凤凰架构》事务处理](https://icyfenix.cn/architect-perspective/general-architecture/transaction/)
- [《凤凰架构》分布式事务](https://icyfenix.cn/architect-perspective/general-architecture/transaction/distributed.html)
- [PostgreSQL: Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
