# 09 Saleor Case Study

> 状态：已完成架构演化证据底稿；具体业务调用链仍按批次制作。

只有学完对应原理后才进入本章。这里不把 2017 写成“落后”，也不把当前版本写成“先进”；只讨论需求、部署和扩展边界变化后，设计权衡为什么改变。

## 固定证据版本

- 当前样本：Saleor tag `3.23.25`，commit `bcb559a79ccafadb21bf9d337ef1dc6b74bd77a2`。
- 历史样本：commit `7e57a29b9f0dd6e93ab77998b93b0d2fe37fcdd6`，提交日期 `2017-12-30`。
- 本地只读目录：`.references/saleor`，不会进入教材 Git 历史。

## 学习顺序

1. `00-current-architecture.md`：先画清当前边界。
2. `01-2017-vs-current.md`：只比较可证实的源码事实。
3. `02-storefront-to-headless.md`：理解 UI 与 Commerce Core 为什么解耦。
4. `03-single-app-to-multi-pod.md`：理解部署变化怎样逼出 stateless、幂等和 `on_commit`。
5. `04-architecture-tradeoffs.md`：回答“为什么不是一开始就这样”。
6. `05-graphql_request_lifecycle.md`：后续制作。
7. `06-data_model_and_indexes.md`：后续制作。
8. `07-checkout_create.md`：后续制作。
9. `08-checkout_complete.md`：后续制作。
10. `09-inventory_allocation.md`：后续制作。
11. `10-payment_flow.md`：后续制作。
12. `11-celery_tasks.md`：后续制作。
13. `12-webhook_events.md`：后续制作。

每个业务案例继续按：原理 → API 入口 → 业务函数 → 模型 → 事务/锁 → 异步事件 → 测试 → 故障 → 面试复述。
