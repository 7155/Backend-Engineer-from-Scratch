# 10 - 用 PEV2 阅读执行计划

终端计划适合精确阅读，树形图适合先看“谁调用谁、耗时集中在哪里”。两者要配合，不能只看最醒目的红色节点。

## 实验器材

- 项目：[dalibo/pev2](https://github.com/dalibo/pev2)
- License：PostgreSQL License
- 离线方式：官方 README 提供 all-in-one `pev2.html`，下载后可直接在浏览器打开，不需要服务器或网络。

教材只链接官方项目，不复制第三方代码。若下载离线 HTML，请同时保留其许可证和来源信息。

## 生成什么

先执行 `10-explain_analyze.sql` 创建实验表，然后在 `psql` 中执行：

```sql
EXPLAIN (ANALYZE, BUFFERS, VERBOSE, FORMAT JSON)
SELECT * FROM planner_events WHERE level = 'ERROR';
```

复制完整 JSON 计划。计划可能包含表名、字段名和查询常量；真实公司 SQL 不要粘贴到公共网站，优先使用离线 `pev2.html`。

## 点击什么、观察什么

1. 打开 PEV2，把 JSON 粘贴到 Plan 输入区并提交。
2. 从根节点向子节点阅读：父节点消费子节点输出，图上的顺序不是 SQL 文本顺序。
3. 找到 `Seq Scan`、`Index Scan` 或 `Bitmap Heap Scan`。
4. 比较 `Plan Rows` 与 `Actual Rows`；差距大说明基数估算不准。
5. 展开节点详情，查看 buffers、loops 和过滤掉的行数。
6. 回到 `10-explain_analyze.sql` 执行 `ANALYZE` 前后的两个计划，观察估算是否更接近实际。

## 为什么会这样

Planner 比较的是整条路径成本，不是“看到索引就必须使用”。返回大量行时，顺序读数据页可能比索引随机定位再回表更便宜；统计信息失真时，planner 也可能基于错误基数选错路径。

## 费曼复述

一个节点显示 `rows=1`，但 `actual rows=100000`。这会怎样影响它上层 Join 的算法选择？你会先检查索引，还是先检查统计信息和数据分布？
