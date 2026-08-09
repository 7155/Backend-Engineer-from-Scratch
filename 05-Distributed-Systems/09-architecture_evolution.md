# 09 - 服务架构演化：单体为什么会走向分布式

```text
V0 单体
→ 代码和部署耦合增长
→ V1 模块化单体
→ 团队/容量边界仍互相影响
→ V2 服务拆分
→ 网络超时与部分失败
→ Timeout / Retry / Circuit Breaker
→ 跨服务事务断裂
→ Saga / Outbox
→ 调用链难观察
→ Trace / Metrics
→ 多实例调度复杂
→ Kubernetes
```

## 为什么单体曾经合理

同一进程调用快、事务边界清楚、部署和调试简单。团队小、流量低、业务边界仍变化时，模块化单体通常比提前拆服务更便宜。

## 服务拆分带来的新物理现实

- 函数异常变成超时、断连和结果未知。
- 重试可能重复写入，因此必须和 idempotency key 配套。
- 本地事务不能覆盖两个数据库。
- 接口版本、鉴权、日志关联和容量规划成为独立成本。

Saleor `3.23.25` 当前证据能证明 API Pod、Celery Worker、共享数据库/Redis 的分布式部署约束，但不能仅凭“多 Pod”断言它是大量业务微服务。Java/Spring 中 Spring Boot 微服务、Resilience4j、Spring Cloud 与 Saga 同样受这些边界约束。

## 停止升级条件

如果模块不能清楚归属、团队不能独立维护、容量无需独立扩展，先保留模块化单体。

费曼题：为什么把一个进程内函数拆成 HTTP 服务后，原来的 try/except 不再足以判断操作失败？

## Sources

- [《凤凰架构》服务架构演进史](https://icyfenix.cn/architecture/architect-history/)
- [《凤凰架构》从类库到服务](https://icyfenix.cn/distribution/connect/)
- [《凤凰架构》服务容错](https://icyfenix.cn/distribution/traffic-management/failure.html)
