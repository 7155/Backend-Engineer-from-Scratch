# 90 - Database 原理映射到 Saleor

这一节只做“原理已经学会之后的源码定位”。Saleor 是 PostgreSQL/Django 生产案例，不是 B+Tree 教学实现。

## 一条真实边界

```text
GraphQL resolver / service
        ↓
Django QuerySet / transaction.atomic
        ↓
PostgreSQL planner、MVCC、锁、索引
        ↓
磁盘 Page 与 Buffer Cache
```

Saleor 负责表达业务查询、约束和事务边界；B+Tree 页分裂、WAL、MVCC 可见性和执行计划由 PostgreSQL 负责。不要在 Python model 中寻找数据库页实现。

## 当前源码观察点

以本地只读 Saleor tag `3.23.25`、commit
`bcb559a79ccafadb21bf9d337ef1dc6b74bd77a2` 为准：

1. `saleor/checkout/models.py`
   - 找 `Checkout` 的字段索引和 `Meta.indexes`。
   - 找 `CheckoutDelivery` 的复合唯一约束，思考它同时承担了什么业务不变量。
   - 找 `Checkout.safe_update`，观察 `transaction.atomic()` 与 `select_for_update()` 如何组合。
2. `saleor/**/migrations/*.py`
   - model 只表达当前状态；migration 才能说明索引何时建立、删除或调整。
3. `saleor/graphql/checkout/` 与 `saleor/checkout/`
   - 从 resolver/mutation 追到 QuerySet，记录实际过滤列、排序列和返回数量。
4. 对同形状的本地 SQL 执行 `EXPLAIN (ANALYZE, BUFFERS)`。

## 一次源码练习

选择一个 checkout 更新入口，按下面顺序记录：

```text
GraphQL 输入
→ resolver / mutation
→ service function
→ QuerySet 条件
→ transaction.atomic 边界
→ select_for_update 锁住的行
→ 相关 model constraint / index
→ 对应测试
```

然后回答：如果两个 Pod 同时更新同一个 checkout，仅靠 Python 进程内的锁为什么无效？数据库行锁在事务提交后什么时候释放？

## 面试表达

- 已实现事实：必须给出当前 checkout 的 commit、文件和函数。
- 已验证证据：测试、实际 SQL 或 `EXPLAIN ANALYZE` 输出。
- 推断：某个业务查询“可能受益于”索引，需要明确说是推断。
- 提议：新增/调整索引必须评估写放大、锁表时间、磁盘空间和查询分布。

本教材不声称教程 SQL 就是 Saleor 线上执行计划；它只提供理解生产源码所需的最小模型。
