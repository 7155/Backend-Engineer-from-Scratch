# 06 - 可观测性演化：日志为什么会变成 Metric + Trace

```text
V0 print
→ 多请求日志混在一起
→ V1 structured log + request_id
→ 多实例无法快速发现趋势
→ V2 metrics + alert
→ 知道慢但不知道慢在哪里
→ V3 distributed trace
→ telemetry 成本过高
→ sampling / retention / SLO
```

## 为什么 print 曾经合理

单进程本地复现时，print 成本最低且上下文就在开发者眼前。只有请求并发、多实例和跨服务出现后，集中检索与关联才成为刚需。

## 三种信号的边界

- Log 保存离散事件和上下文，但高基数搜索昂贵。
- Metric 适合聚合趋势和告警，但不能还原单次调用链。
- Trace 展示 span 因果和关键路径，但采样可能漏掉稀有问题。

Saleor `3.23.25` 依赖 OpenTelemetry，并在 GraphQL 路径记录请求和查询成本相关信息；这证明 instrumentation 存在，不证明某个生产环境的采样率、SLO 或保存周期。Spring 对应 Micrometer、Actuator、OpenTelemetry Java Agent。

## 为什么小项目不直接全量 Trace

全量 telemetry 消耗 CPU、网络、存储和排障注意力。没有明确问题和保留策略时，先从结构化日志与少量核心指标开始。

费曼题：P99 延迟告警已经触发，为什么只有 Metric 仍可能无法判断慢在数据库、Redis 还是下游 HTTP？

## Sources

- [《凤凰架构》可观测性](https://icyfenix.cn/distribution/observability/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
