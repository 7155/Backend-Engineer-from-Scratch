-- 09 - EXPLAIN ANALYZE：成本估算如何变成真实执行
--
-- EXPLAIN 只展示 planner 的估算；EXPLAIN ANALYZE 会真正执行语句，并补上 actual。
-- 对 UPDATE/DELETE 使用 ANALYZE 会真的改数据，生产环境必须先确认语句影响。

\timing on

DROP TABLE IF EXISTS planner_events;
CREATE TABLE planner_events (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    level text NOT NULL,
    source text NOT NULL,
    created_at timestamptz NOT NULL
);

INSERT INTO planner_events (level, source, created_at)
SELECT
    CASE WHEN value % 100 = 0 THEN 'ERROR' ELSE 'INFO' END,
    'service-' || value % 20,
    timestamptz '2025-01-01 00:00:00+00' + value * interval '1 second'
FROM generate_series(1, 200000) AS value;

CREATE INDEX idx_planner_events_level ON planner_events (level);
ANALYZE planner_events;

\echo '1) ERROR 约占 1%：选择性高，索引更有价值'
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM planner_events WHERE level = 'ERROR';

\echo '2) INFO 约占 99%：回表代价可能比顺序扫描更高'
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM planner_events WHERE level = 'INFO';

\echo '3) 修改大量数据但暂不 ANALYZE：统计信息可能落后于现实'
UPDATE planner_events SET level = 'ERROR' WHERE id % 2 = 0;
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM planner_events WHERE level = 'ERROR';

\echo '4) 刷新统计信息后，estimated rows 应更接近 actual rows'
ANALYZE planner_events;
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM planner_events WHERE level = 'ERROR';

\echo '5) 查看 planner 记录的常见值与频率'
SELECT attname, n_distinct, most_common_vals, most_common_freqs
FROM pg_stats
WHERE schemaname = 'public' AND tablename = 'planner_events';

-- 练习题：为什么“建了索引却不走”可能是正确选择，也可能是统计信息过期？