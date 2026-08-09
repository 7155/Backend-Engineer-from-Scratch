# 制作与学习进度

## 第一批教材文件

- [x] `00-Computer/01-process_thread_coroutine.py`
- [x] `00-Computer/02-cpu_bound_vs_io_bound.py`
- [x] `00-Computer/03-event_loop_visual.html`
- [x] `00-Computer/04-concurrency_evolution.md`
- [x] `01-Web/01-http_message.py`
- [x] `01-Web/02-tiny_http_server.py`
- [x] `01-Web/03-http_server_evolution.md`
- [x] `01-Web/04-wireshark_visual.md`
- [x] `02-Database/01-page_io.py`
- [x] `02-Database/02-buffer_pool.py`
- [x] `02-Database/03-btree.py`
- [x] `02-Database/04-bplus_tree.py`
- [x] `02-Database/05-bplus_tree_visual.md`
- [x] `02-Database/06-index_basic.sql`
- [x] `02-Database/07-index_evolution.md`
- [x] `02-Database/08-composite_index.sql`
- [x] `02-Database/09-query_planner.py`
- [x] `02-Database/10-explain_analyze.sql`
- [x] `02-Database/11-explain_visual.md`

这里的勾选只表示教材已制作并通过自动检查，不代表学习者已经掌握。

## Engineering Evolution 底稿

- [x] 并发：`00-Computer/04-concurrency_evolution.md`
- [x] Web：`01-Web/03-http_server_evolution.md`
- [x] 数据库索引：`02-Database/07-index_evolution.md`
- [x] 数据库事务：`02-Database/12-transaction_evolution.md`（后续实验骨架）
- [x] 缓存：`03-Redis/04-cache_evolution.md`
- [x] MQ：`04-Message-Queue/07-message_queue_evolution.md`
- [x] 服务架构：`05-Distributed-Systems/09-architecture_evolution.md`
- [x] 交易：`06-Transaction-Systems/09-transaction_evolution.md`
- [x] 可观测性：`07-Testing-Observability/06-observability_evolution.md`
- [x] 部署：`08-Deployment/08-deployment_evolution.md`
- [x] Saleor 历史演化：`09-Saleor-Case-Study/00` 到 `04`

## 个人学习过关条件

每个编号文件单独检查：

- [ ] Demo/实验亲自跑通。
- [ ] 能从 V0 解释核心原理。
- [ ] 能说出一个触发升级的故障信号。
- [ ] 能说出新方案新增的一项成本。
- [ ] 能指出 Saleor 对应源码和证据等级。
- [ ] 能独立回答该文件唯一的费曼题。

## 已验证环境

- [x] Python 3.12 `.venv`、`uv.lock` 和 Ruff 已准备。
- [x] PostgreSQL 16 与 Redis 7 容器健康，端口分别为 `55432` 和 `56379`。
- [x] HTTP、订单和复合索引 fixture 已按固定 seed 生成，并带 SHA-256 manifest。
- [x] 三份 PostgreSQL SQL 已实际执行，每张实验表 20 万行。
- [x] Redis 已写入 String、List、Set、Sorted Set、Stream 五类 `backend-lab:` 教学数据。
- [x] Saleor 只读参考固定为 tag `3.23.25` / commit `bcb559a79ccafadb21bf9d337ef1dc6b74bd77a2`。

## 仍需手工验收

- [ ] Wireshark 需要本机抓包权限。
- [ ] Chalmers B+Tree Visualizer 与 PEV2 需要手工浏览器观察。
- [ ] Saleor 具体 Checkout、库存、支付、Webhook 流程尚未完成函数级调用链。
