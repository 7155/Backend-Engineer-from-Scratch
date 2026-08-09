# 03 Redis & Cache

> 状态：路线骨架。

目标：理解缓存边界和失败模式，不停在 `SET/GET`。

## 计划顺序

1. `01-why_cache.py`：延迟、吞吐、命中率与引入成本。
2. `02-cache_aside.py`：读 miss、回源、写库、失效。
3. `03-cache_consistency_race.py`：复现数据库更新与缓存失效竞态。
4. `04-redis_commander_visual.md`：观察 Key、Value、TTL 和数据结构。
5. `05-penetration_breakdown_avalanche.py`：布隆过滤、singleflight、随机 TTL。
6. `06-hot_key_big_key.py`：请求倾斜与阻塞。
7. `07-lua_atomicity.py`：服务端原子脚本。
8. `08-distributed_lock.py`：租约、token、续期与 fencing。
9. `09-token_bucket.py`：限流。
10. `90-saleor_mapping.md`：缓存 owner、失效和多 Pod 边界。

Visual Lab 计划使用 [Redis Commander](https://github.com/joeferner/redis-commander)（MIT），只连接本地教学 Redis。
