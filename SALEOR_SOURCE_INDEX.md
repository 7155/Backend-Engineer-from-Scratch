# Saleor Source Index

固定参考：Saleor `3.23.25` / `bcb559a79ccafadb21bf9d337ef1dc6b74bd77a2`。历史对比：`7e57a29b9f0dd6e93ab77998b93b0d2fe37fcdd6`。

| 教材知识点 | Saleor 文件与 symbol | 事务/锁/异步 | 对应测试 | 状态 |
| --- | --- | --- | --- | --- |
| GraphQL 请求入口 | `saleor/graphql/views.py:GraphQLView.dispatch`；`saleor/graphql/api.py:schema` | View 进入 resolver 后再定位事务 | 待按具体 operation 建索引 | 已读入口 |
| Checkout 索引 | `saleor/checkout/models.py:Checkout.Meta.indexes` | PostgreSQL Planner 决定执行路径 | migration/model 测试待定位 | 已读定义 |
| Checkout 安全更新 | `saleor/checkout/models.py:Checkout.safe_update` | `transaction.atomic` + `select_for_update` | checkout model tests 待定位 | 已读实现 |
| Checkout/Line 行锁 | `saleor/checkout/lock_objects.py` | 按 `pk` 排序后 `select_for_update` | 并发测试待定位 | 已读实现 |
| Checkout Create | `saleor/graphql/checkout/mutations/checkout_create.py:CheckoutCreate` | 调用链待逐步追踪 | 对应 mutation tests 待定位 | 已确认入口 |
| Checkout Complete | `saleor/graphql/checkout/mutations/checkout_complete.py:CheckoutComplete`；`saleor/checkout/complete_checkout.py:complete_checkout*` | 事务、库存、支付分支待逐步追踪 | complete checkout tests 待定位 | 已确认入口 |
| Celery runtime | `saleor/celeryconf.py:app`；`saleor/settings.py:CELERY_*` | `AGENTS.md` 要求 `on_commit`、幂等与可重试 | task tests 待按模块定位 | 已读配置 |
| 多 Pod 模型 | `AGENTS.md:Deployment model` | shared PostgreSQL/read replicas + Redis/broker | 需要部署/运行证据 | 已读契约 |
| Storefront → Headless | 当前/历史 `README.md`；历史 `saleor/dashboard/` 树 | 网络扩展引入独立失败边界 | 不是单元测试结论 | 已做差异比较 |

“待定位”表示尚未完成源码调用链，不允许用目录名或预期行为补写结论。
