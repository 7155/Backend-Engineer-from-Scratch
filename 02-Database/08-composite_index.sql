-- 07 - 复合索引与最左前缀
--
-- 索引：(user_id, status, created_at)
-- B+Tree 先按 user_id 排序；同一 user_id 内再按 status；前两项都相同时才按 created_at。
-- 因此它不是三个互相独立的单列索引。

\timing on

DROP TABLE IF EXISTS composite_orders;
CREATE TABLE composite_orders (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id integer NOT NULL,
    status text NOT NULL,
    created_at timestamptz NOT NULL,
    total_cents integer NOT NULL
);

INSERT INTO composite_orders (user_id, status, created_at, total_cents)
SELECT
    value % 1000,
    -- status 按同一 user_id 的“第几轮”变化，避免 user_id 与 status 完全相关。
    (ARRAY['NEW', 'PAID', 'SHIPPED', 'CANCELLED'])[1 + (value / 1000) % 4],
    timestamptz '2025-01-01 00:00:00+00' + value * interval '1 second',
    1000 + value % 100000
FROM generate_series(1, 200000) AS value;

CREATE INDEX idx_composite_orders_user_status_created
ON composite_orders (user_id, status, created_at);
ANALYZE composite_orders;

\echo '1) 使用第一列 user_id：满足最左前缀'
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM composite_orders WHERE user_id = 17;

\echo '2) 使用 user_id + status：继续缩小有序区间'
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM composite_orders WHERE user_id = 17 AND status = 'PAID';

\echo '3) 只查 status：跳过最左列，通常不能高效定位索引区间'
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM composite_orders WHERE status = 'PAID';

\echo '4) 等值前缀后接 created_at 范围：三列都能参与定位'
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM composite_orders
WHERE user_id = 17
  AND status = 'PAID'
  AND created_at >= timestamptz '2025-01-02 00:00:00+00';

\echo '5) 范围列之后再加条件：后续列常用于过滤，而不是继续缩小连续区间'
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM composite_orders
WHERE user_id > 900
  AND status = 'PAID';

\echo '6) 前缀固定后按 created_at 排序：索引顺序可以避免额外 Sort'
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, created_at
FROM composite_orders
WHERE user_id = 17 AND status = 'PAID'
ORDER BY created_at
LIMIT 20;

-- 观察任务：在计划中区分 Index Cond、Filter 和 Sort。
-- 费曼问题：为什么 (user_id, status, created_at) 很难直接服务 WHERE status = ?？
