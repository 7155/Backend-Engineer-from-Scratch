# 05 Distributed Systems

> 状态：路线骨架。

目标：解释为什么超时不等于失败、重试必须配幂等、多实例不能依赖本地状态。

## 计划顺序

1. `01-check_then_act_race.py`
2. `02-optimistic_pessimistic_lock.py`
3. `03-idempotency_key.py`
4. `04-timeout_unknown_result.py`
5. `05-retry_storm.py`
6. `06-circuit_breaker.py`
7. `07-backpressure.py`
8. `08-cap_consistency.py`
9. `09-architecture_evolution.md`：单体 → 模块化单体 → 服务拆分 → 分布式治理。
10. `10-retry_visual.html`：本地离线状态变化图。
11. `90-saleor_mapping.md`
