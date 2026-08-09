-- 06 - 第一个 PostgreSQL 索引实验
--
-- 现实问题：WHERE user_id = 4242 为什么可能扫描整张表？
-- 核心规则：索引用额外空间维护“可快速定位的 key -> 行位置”，让数据库少读数据页。
--
-- 运行：
--   docker compose up -d postgres
--   docker compose exec -T postgres psql -U backend_lab -d backend_lab \
--     < 02-Database/06-index_basic.sql

\timing on

DROP TABLE IF EXISTS index_lab_orders;
CREATE TABLE index_lab_orders (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id integer NOT NULL,
    status text NOT NULL,
    created_at timestamptz NOT NULL,
    payload text NOT NULL
);

-- 20 万行足够让本地实验看到计划差异，又不会把教材变成压测工程。
INSERT INTO index_lab_orders (user_id, status, created_at, payload)
SELECT
    value % 10000,
    (ARRAY['NEW', 'PAID', 'SHIPPED', 'CANCELLED'])[1 + value % 4],
    timestamptz '2025-01-01 00:00:00+00' + value * interval '1 second',
    repeat('x', 80)
FROM generate_series(1, 200000) AS value;

ANALYZE index_lab_orders;

\echo '1) 没有 user_id 索引：通常需要 Seq Scan'
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM index_lab_orders WHERE user_id = 4242;

CREATE INDEX idx_index_lab_orders_user_id
ON index_lab_orders (user_id);
ANALYZE index_lab_orders;

\echo '2) 创建索引后：通常变成 Bitmap/Index Scan，实际选择由 planner 决定'
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM index_lab_orders WHERE user_id = 4242;

\echo '3) 索引不覆盖 created_at：这个条件仍可能 Seq Scan'
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM index_lab_orders
WHERE created_at >= timestamptz '2025-01-03 00:00:00+00';

-- 观察任务：不要只比较 Execution Time，还要比较 actual rows 和 shared hit/read blocks。
-- 面试追问：有索引后，为什么 PostgreSQL 仍可能选择 Seq Scan？
