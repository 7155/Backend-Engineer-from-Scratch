# 制作进度

## 第一批：完整

- `00-Computer/01-process_thread_coroutine.py`
- `00-Computer/02-cpu_bound_vs_io_bound.py`
- `00-Computer/03-event_loop_visual.html`
- `01-Web/01-http_message.py`
- `01-Web/02-tiny_http_server.py`
- `01-Web/03-wireshark_visual.md`
- `02-Database/01-page_io.py`
- `02-Database/02-buffer_pool.py`
- `02-Database/03-btree.py`
- `02-Database/04-bplus_tree.py`
- `02-Database/05-bplus_tree_visual.md`
- `02-Database/06-index_basic.sql`
- `02-Database/07-composite_index.sql`
- `02-Database/08-query_planner.py`
- `02-Database/09-explain_analyze.sql`
- `02-Database/10-explain_visual.md`

每个完整章还有一个 `90-saleor_mapping.md`。

## 后续：路线骨架

`03-Redis` 到 `10-Interview` 当前只写章节 README、顺序和 Visual Lab 计划。不会在验证前一次生成整本书。

## 已验证环境

- Python 3.12 `.venv`、`uv.lock` 和 PostgreSQL 18 客户端已经准备完成。
- 第一批 HTTP、订单和复合索引查询 fixture 已按固定 seed 生成，并带 SHA-256 manifest。
- PostgreSQL 16 与 Redis 7 容器健康，分别映射 `55432` 和 `56379`。
- 三份 PostgreSQL SQL 已实际执行，每张实验表 20 万行；执行计划保存在 `.lab/results/`。
- Redis 已写入 String、List、Set、Sorted Set、Stream 五类 `backend-lab:` 教学数据。
- Python 自检、Ruff lint/format、学习数据 manifest 和 PEV2 JSON 计划均已通过。

## 尚未验证

- Saleor 尚未本地 checkout 固定 commit；章末映射仍以已核验的官方网页源码为边界。
- Wireshark 需要本机抓包权限，PEV2/外部 Visual Lab 需要手工浏览器验收。
