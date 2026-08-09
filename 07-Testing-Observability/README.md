# 07 Testing, Observability & Performance

> 状态：路线骨架。

目标：用测试证明不变量，用 Log/Metric/Trace 定位问题，用 P95/P99 表达用户体验。

## 计划顺序

1. `01-unit_integration_e2e.py`
2. `02-concurrency_test.py`
3. `03-structured_log.py`
4. `04-metric.py`
5. `05-trace.py`
6. `06-observability_evolution.md`：print → structured log → metric → trace → SLO。
7. `07-jaeger_visual.md`
8. `08-n_plus_one.py`
9. `09-load_test.py`
10. `10-p95_p99.py`
11. `90-saleor_mapping.md`

Visual Lab：先用 Jaeger all-in-one 看单条 Trace；再用 OpenTelemetry Astronomy Shop 看多服务 Span、关键路径和错误传播。
