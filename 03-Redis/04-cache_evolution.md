# 04 - 缓存演化：DB → Local Cache → Redis

```text
V0 每次查询 DB
→ 热点读压垮共享数据库
→ V1 进程内 Dict/LRU
→ 多实例缓存各不相同
→ V2 Redis 共享缓存
→ DB 更新后缓存仍旧
→ V3 Cache Aside
→ 穿透、击穿、雪崩、Hot Key
→ V4 限流、singleflight、随机 TTL、高可用
```

## 为什么 V0/V1 曾经合理

低 QPS 时直接查 DB 只有一个真相源；单实例时本地 LRU 延迟最低、没有网络和序列化成本。部署第二个实例前，共享 Redis 可能只是额外故障点。

## 每次优化制造的新问题

- Redis 让实例共享缓存，也引入网络、容量、淘汰和高可用问题。
- Cache Aside 降低数据库读压，却不能免费保证 DB 与 cache 原子一致。
- 长 TTL 减少回源但增加陈旧时间；短 TTL 更新快却增加 miss。
- 防击穿锁避免重复重建，却可能造成等待、锁过期和热点转移。

## 为什么 Redis 不能替代数据库

缓存允许 miss、淘汰和重建；交易真相需要约束、事务、持久性和查询能力。除非业务明确把 Redis 设计为权威存储，否则它只是派生数据。

## Saleor 与 Java/Spring

Saleor `3.23.25` 的多 Pod 模型要求共享 Redis/broker，但当前文件还不能证明每个业务对象都使用缓存。制作完整章时必须逐个追 key owner 和失效路径。Spring 对应 Caffeine 本地缓存、Spring Cache/RedisTemplate 共享缓存；注解不会自动解决一致性。

## 停止升级条件

如果数据库容量充足、查询已优化、陈旧数据不可接受或 key 很少复用，先不加缓存。

费曼题：为什么从单实例扩成两实例，会让一个原本正确的本地 LRU 突然产生用户可见的不一致？

## Sources

- [Redis 官方文档](https://redis.io/docs/latest/)
- [Redis client-side caching](https://redis.io/docs/latest/develop/reference/client-side-caching/)
- [《凤凰架构》服务端缓存](https://icyfenix.cn/architect-perspective/general-architecture/diversion-system/cache-middleware.html)
