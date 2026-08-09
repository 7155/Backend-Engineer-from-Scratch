# Source Index

教材遵循：**权威教材/官方资料 → 可运行实验 → 固定版本生产源码 → AI 重新组织与出题**。

引用来源不等于照抄来源。每个编号文件只提取当前问题需要的机制，改写成短解释，并用本地实验或 Saleor 源码验证。无法验证的内容标记“需要验证”。

## 课程形式

- [juliepy/AI-Engineer-from-scrach](https://github.com/juliepy/AI-Engineer-from-scrach)：只参考编号章节、单文件递进和可运行 Demo 的组织形式。
- 本地结构核验：`02-RAG/02-RAG_basic/01…12` 按文件编号逐步推进；不复制其代码或教材内容。

## 工程演化主教材

- [《凤凰架构》官方网站](https://icyfenix.cn/)
- [服务架构演进史](https://icyfenix.cn/architecture/architect-history/)
- [从类库到服务](https://icyfenix.cn/distribution/connect/)
- [事务处理](https://icyfenix.cn/architect-perspective/general-architecture/transaction/)
- [分布式事务](https://icyfenix.cn/architect-perspective/general-architecture/transaction/distributed.html)
- [服务端缓存](https://icyfenix.cn/architect-perspective/general-architecture/diversion-system/cache-middleware.html)
- [服务容错](https://icyfenix.cn/distribution/traffic-management/failure.html)
- [可观测性](https://icyfenix.cn/distribution/observability/)
- [以容器构建系统](https://icyfenix.cn/immutable-infrastructure/container/container-build-system.html)
- 官方站点确认的源码仓库：[fenixsoft/awesome-fenix](https://github.com/fenixsoft/awesome-fenix)

用途：回答“为什么演化”，不机械复刻目录，不复制大段原文。网站声明文档采用 CC BY-NC-SA 4.0；本教材当前只做链接、短摘要和独立实验。

## 00 Computer / 01 Web

- [Python `threading`](https://docs.python.org/3/library/threading.html)
- [Python `multiprocessing`](https://docs.python.org/3/library/multiprocessing.html)
- [Python `asyncio`](https://docs.python.org/3/library/asyncio.html)
- [Python `socket`](https://docs.python.org/3/library/socket.html)
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)
- [ASGI specification](https://asgi.readthedocs.io/en/latest/specs/main.html)

## 02 Database

- [PostgreSQL: Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL: Multicolumn Indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
- [PostgreSQL: Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [PostgreSQL: Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html)
- [CMU 15-445/645 Database Systems](https://15445.courses.cs.cmu.edu/fall2025/)

PostgreSQL 文档负责实际 planner、MVCC 与锁语义；CMU 课程负责 storage/page/index/concurrency 的系统模型；本地 Python/SQL 实验负责观察。教学 B+Tree 不是 PostgreSQL 内部实现的复制品。

## 03 Redis

- [Redis 官方文档](https://redis.io/docs/latest/)
- [Redis client-side caching](https://redis.io/docs/latest/develop/reference/client-side-caching/)
- [Redis persistence](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/)
- 《凤凰架构》[服务端缓存](https://icyfenix.cn/architect-perspective/general-architecture/diversion-system/cache-middleware.html)

## 04 Message Queue

- [RabbitMQ Reliability Guide](https://www.rabbitmq.com/docs/reliability)
- [RabbitMQ Consumer Acknowledgements](https://www.rabbitmq.com/docs/confirms)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Celery Tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html)

ACK、redelivery、retry 和 idempotency 必须按具体 broker/client 语义说明，不能把 RabbitMQ、Kafka 和 Celery 混成同一种保证。

## 05 Distributed / 06 Transaction

- 《凤凰架构》[从类库到服务](https://icyfenix.cn/distribution/connect/)
- 《凤凰架构》[服务容错](https://icyfenix.cn/distribution/traffic-management/failure.html)
- 《凤凰架构》[事务处理](https://icyfenix.cn/architect-perspective/general-architecture/transaction/)
- 《凤凰架构》[分布式事务](https://icyfenix.cn/architect-perspective/general-architecture/transaction/distributed.html)
- PostgreSQL 官方事务与锁文档见数据库部分。

## 07 Observability / 08 Deployment

- 《凤凰架构》[可观测性](https://icyfenix.cn/distribution/observability/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Kubernetes Concepts](https://kubernetes.io/docs/concepts/)
- [Kubernetes Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)

## 09 Saleor Production Case

- [Saleor 官方仓库](https://github.com/saleor/saleor)
- 教材固定 tag `3.23.25`，commit `bcb559a79ccafadb21bf9d337ef1dc6b74bd77a2`。
- 历史比较固定 commit `7e57a29b9f0dd6e93ab77998b93b0d2fe37fcdd6`。
- 函数级阅读状态见 `SALEOR_SOURCE_INDEX.md`；只读规则见 `SALEOR_REFERENCE.md`。

## 来源进入教材前的检查

- [ ] 链接是否来自官方站点、标准组织、大学课程或固定生产仓库？
- [ ] 结论是否能被一个实验或源码位置观察？
- [ ] 是否把数据库/框架版本差异说清？
- [ ] 是否把事实、推断、建议和“需要验证”分开？
- [ ] 是否避免大段引用和未经许可复制第三方代码/图片？
