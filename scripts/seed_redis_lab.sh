#!/usr/bin/env bash
set -euo pipefail

backend_lab_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
result_dir="$backend_lab_root/.lab/results"
mkdir -p "$result_dir"

"$backend_lab_root/scripts/start_services.sh" >/dev/null

redis() {
  docker compose --project-directory "$backend_lab_root" exec -T redis redis-cli "$@"
}

# 只清理本教材拥有的固定 key，不使用 FLUSHDB，不影响其他项目。
redis DEL \
  backend-lab:product:42 \
  backend-lab:cart:7 \
  backend-lab:tags:42 \
  backend-lab:ranking \
  backend-lab:events >/dev/null

redis SET backend-lab:product:42 \
  '{"id":42,"name":"B+Tree Notebook","price_cents":2999}' EX 3600 >/dev/null
redis RPUSH backend-lab:cart:7 product:42 product:9 product:42 >/dev/null
redis SADD backend-lab:tags:42 database index interview >/dev/null
redis ZADD backend-lab:ranking 98 user:17 87 user:42 73 user:9 >/dev/null
redis XADD backend-lab:events 1-0 type checkout.created checkout_id 1001 >/dev/null
redis XADD backend-lab:events 2-0 type payment.authorized checkout_id 1001 >/dev/null

{
  echo "product=$(redis GET backend-lab:product:42)"
  echo "product_ttl=$(redis TTL backend-lab:product:42)"
  echo "cart_length=$(redis LLEN backend-lab:cart:7)"
  echo "tag_count=$(redis SCARD backend-lab:tags:42)"
  echo "ranking_count=$(redis ZCARD backend-lab:ranking)"
  echo "event_count=$(redis XLEN backend-lab:events)"
} | tee "$result_dir/redis_seed.txt"
