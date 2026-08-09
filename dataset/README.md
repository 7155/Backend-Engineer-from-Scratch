# Learning Data

这里不保存个人数据，也不复制 Saleor 生产数据。所有内容都由固定 seed 生成，可以删除并重新创建。

准备数据：

```bash
source scripts/activate_lab.sh
python scripts/prepare_learning_data.py
python scripts/prepare_learning_data.py --check
```

输出统一放在被 Git 忽略的 `.lab/learning-data/`：

```text
http/
├── 01-health.http
├── 02-echo.http
└── 03-json.http

database/
├── orders_small.csv
└── query_cases.json

manifest.json
```

- HTTP 文件保留真实 `CRLF`，用于 `01-Web` 的 parser/socket 实验。
- `orders_small.csv` 有 1,000 条确定性订单，适合先手工观察复合列分布。
- `query_cases.json` 给出 `(user_id, status, created_at)` 的查询形状，但不替你判断执行计划。
- PostgreSQL Planner 实验需要更大数据量；`02-Database/*.sql` 会在数据库内部用 `generate_series` 生成 20 万行，避免仓库长期保存大型 CSV。
- `manifest.json` 记录 seed、大小和 SHA-256，用于证明数据没有静默变化。
- Redis seed 使用 `backend-lab:` 命名空间，包含 String、List、Set、Sorted Set 和 Stream；脚本只重建这些固定 key。

把 fixture 喂给真实课程代码：

```bash
python 01-Web/01-http_message.py \
  --request-file .lab/learning-data/http/02-echo.http
```

先观察小订单分布，再运行 20 万行的 PostgreSQL 实验：

```bash
python -c 'import csv; from collections import Counter; rows=list(csv.DictReader(open(".lab/learning-data/database/orders_small.csv"))); print(Counter(r["status"] for r in rows))'
scripts/run_database_labs.sh
```

这些都是学习 fixture，不代表真实流量、真实用户分布或 Saleor 生产指标。
