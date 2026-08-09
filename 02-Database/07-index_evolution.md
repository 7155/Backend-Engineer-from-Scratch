# 07 - 索引为什么会演化成 B+Tree + Query Planner

## V0：全表扫描

一百行订单全部扫描一次，代码简单、写入便宜，也不会维护额外结构。数据能放进少量 Page、查询频率低时，全表扫描就是正确方案。

```text
数据增长
→ 扫描 Page 数持续增长
→ 随机磁盘 I/O 比 CPU 比较昂贵
→ 需要减少访问 Page 数
```

## 从 BST 到 B+Tree

| 版本 | 为什么出现 | 解决了什么 | 新代价 |
| --- | --- | --- | --- |
| BST | 用有序结构避免扫描全部 key | 平均点查变快 | 节点窄、树可能很高或退化 |
| B-Tree | 一个 Page 放很多 key/child | fan-out 大，树高降低 | split 会修改多个节点 |
| B+Tree | 内部节点主要导航，完整记录在叶子 | 内部层更紧凑，叶子链支持范围扫描 | 点查最终仍到叶子，维护更复杂 |
| Secondary Index | 不只按主键查询 | 支持更多访问路径 | 回表、额外空间、写放大 |
| Composite Index | 一个有序结构匹配多列过滤/排序 | 减少候选和额外 Sort | 列顺序绑定查询形状 |
| Query Planner | 有索引不代表使用它更便宜 | 按基数、选择性和成本选路径 | 依赖统计信息，估算可能失真 |

## 一次 Page I/O 推导

假设每个内部 Page 能指向 200 个孩子：

```text
高度 1：200 个叶子
高度 2：40,000 个叶子
高度 3：8,000,000 个叶子
```

高 fan-out 让海量记录仍只需少量层级定位。真实数据库还会受到 Buffer Pool、Page fill factor、记录大小和缓存命中影响，因此这里是数量级模型，不是 PostgreSQL 固定承诺。

## 优化又制造了什么问题

- 每个 INSERT/UPDATE/DELETE 都可能维护多个索引。
- 随机写、Page split、WAL 和 Vacuum 带来写放大。
- 低选择性查询可能读取大量索引项再回表，比 Seq Scan 更贵。
- 复合索引列序不匹配查询时，空间成本存在但收益很低。
- 统计信息陈旧会让 Planner 错估 rows。

运行 `06-index_basic.sql` 可以观察同一查询从 Seq Scan 变成 Bitmap Index Scan；运行 `08-composite_index.sql` 可以观察只查 `status` 时仍选择 Seq Scan。

## 为什么不给每个字段都建索引

因为读优化不是免费的。只有真实慢查询、查询频率、选择性和写入成本共同证明收益时才建；小表、低频查询或写密集字段可能更适合扫描。

## B+Tree 为什么不是 Hash 的完全替代

Hash 适合等值定位，但天然不提供 key 顺序；B+Tree 同时支持等值、范围和排序，是更通用的索引。某些等值热点仍可能适合 Hash Index，这取决于数据库实现与 workload。

## LSM Tree 预告

LSM 把随机写转成内存写与顺序合并，适合写密集场景；代价是 compaction、读放大和空间放大。它不是“比 B+Tree 新”，而是另一组读写权衡。

## Saleor 位于哪一层

Saleor `3.23.25` 的 `saleor/checkout/models.py` 定义字段索引、`Meta.indexes` 和约束；QuerySet 交给 PostgreSQL Planner。Saleor 表达业务访问路径，PostgreSQL 负责 B+Tree Page、统计信息和执行计划。

## Java/Spring 与数据库术语

- JPA/Hibernate 的 `@Index`、Django `Meta.indexes` 最终都生成数据库 DDL。
- MySQL/InnoDB 常讨论聚簇主键与二级索引回表；PostgreSQL heap/index 组织不同，但同样要看覆盖、选择性和回表成本。
- 框架方法名不能证明走索引，必须看真实 SQL 与 `EXPLAIN ANALYZE`。

## 费曼复述

从“小表全扫完全合理”开始，解释系统为什么最终需要 B+Tree、复合索引和 Query Planner，并说出在哪三种情况下你会拒绝新增索引。

## Sources

- [CMU 15-445/645 Database Systems](https://15445.courses.cs.cmu.edu/fall2025/)
- [PostgreSQL: Multicolumn Indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
- [PostgreSQL: Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
