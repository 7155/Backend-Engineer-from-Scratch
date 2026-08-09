# 02 Database Internals

这是第一重点章。目标不是背“B+Tree、最左前缀”，而是把 Page I/O、树高、叶子顺序、查询边界和 planner cost 连成一条链。

## 学习顺序

1. `01-page_io.py`：数据库为何按固定 Page 搬运数据。
2. `02-buffer_pool.py`：五次逻辑读取为何只产生三次底层读取。
3. `03-btree.py`：普通二叉树为何层数高，高扇出解决什么。
4. `04-bplus_tree.py`：手写 insert/search/split/leaf link/range scan。
5. `05-bplus_tree_visual.md`：用 Chalmers 动画亲眼看 leaf/root split。
6. `06-index_basic.sql`：第一次在 PostgreSQL 建索引并看计划。
7. `07-composite_index.sql`：最左前缀、范围截断、排序。
8. `08-query_planner.py`：用 toy cost 理解 Seq Scan 与 Index Scan 的交叉点。
9. `09-explain_analyze.sql`：看 estimated/actual rows、Buffers 和旧统计信息。
10. `10-explain_visual.md`：把计划粘进离线 PEV2。
11. `90-saleor_mapping.md`：再追 Saleor Model/Migration/QuerySet/SQL。

Python 自检：

```bash
python3 02-Database/01-page_io.py
python3 02-Database/02-buffer_pool.py
python3 02-Database/03-btree.py
python3 02-Database/04-bplus_tree.py
python3 02-Database/08-query_planner.py
```

PostgreSQL：

```bash
docker compose up -d postgres
docker compose exec -T postgres psql -U backend_lab -d backend_lab < 02-Database/06-index_basic.sql
docker compose exec -T postgres psql -U backend_lab -d backend_lab < 02-Database/07-composite_index.sql
docker compose exec -T postgres psql -U backend_lab -d backend_lab < 02-Database/09-explain_analyze.sql
```

## 国内面试关键词

Page、Buffer Pool、B/B+Tree、聚簇/二级索引、回表、覆盖索引、最左前缀、Cardinality、Selectivity、Seq/Index/Bitmap Scan、统计信息。

## 费曼复述

> 从“磁盘一次搬一页”开始，解释为什么 B+Tree 要高扇出、数据放叶子、叶子相连；再说明 `(user_id,status,created_at)` 为什么只查 status 通常不能直接 seek，以及 planner 为什么仍可能放弃已有索引。
