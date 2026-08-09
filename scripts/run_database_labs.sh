#!/usr/bin/env bash
set -euo pipefail

backend_lab_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="$backend_lab_root/.venv/bin:/opt/homebrew/opt/libpq/bin:$PATH"

if ! command -v pg_isready >/dev/null 2>&1 || \
   ! pg_isready -h 127.0.0.1 -p 55432 -U backend_lab -d backend_lab >/dev/null 2>&1; then
  "$backend_lab_root/scripts/start_services.sh"
fi

if ! command -v psql >/dev/null 2>&1; then
  echo "ERROR: 缺少 psql 客户端。" >&2
  exit 1
fi

sql_lessons=(
  "02-Database/06-index_basic.sql"
  "02-Database/07-composite_index.sql"
  "02-Database/09-explain_analyze.sql"
)

result_dir="$backend_lab_root/.lab/results"
mkdir -p "$result_dir"

for lesson in "${sql_lessons[@]}"; do
  echo
  echo "Running $lesson"
  result_name="$(basename "$lesson" .sql).txt"
  PGPASSWORD=backend_lab_only psql -v ON_ERROR_STOP=1 \
    -h 127.0.0.1 -p 55432 -U backend_lab -d backend_lab \
    < "$backend_lab_root/$lesson" | tee "$result_dir/$result_name"
done

PGPASSWORD=backend_lab_only psql -X -q -A -t \
  -h 127.0.0.1 -p 55432 -U backend_lab -d backend_lab \
  -c "EXPLAIN (ANALYZE, BUFFERS, VERBOSE, FORMAT JSON) SELECT * FROM planner_events WHERE level = 'ERROR';" \
  > "$result_dir/planner_events_error.plan.json"

echo
echo "Database labs completed. Results: $result_dir"
