# Backend-Engineer-from-Scratch

这是一个 Juliepy 风格的后端原理教材：每章一个目录，一个编号文件解决一个核心概念，按文件名从 01 一路运行。

```text
最简单方案 → 为什么曾经合理 → 规模化故障 → 第一次优化
→ 新问题 → 继续演化 → 原理 → Demo → Visual Lab
→ Saleor → Trade-off → 面试 → 费曼复述
```

主线规范见 [ENGINEERING_EVOLUTION.md](ENGINEERING_EVOLUTION.md)。基础设施不是凭空出现的；它通常是上一代方案规模化后暴露的问题逼出来的。

## 为什么这样组织

学习 B+Tree 时只需要依次打开：

```text
02-Database/03-btree.py
02-Database/04-bplus_tree.py
02-Database/05-bplus_tree_visual.md
02-Database/06-index_basic.sql
02-Database/07-index_evolution.md
02-Database/08-composite_index.sql
02-Database/09-query_planner.py
02-Database/10-explain_analyze.sql
02-Database/11-explain_visual.md
02-Database/90-saleor_mapping.md
```

代码注释负责讲原理、输入、执行步骤、故障和面试点；README 只做导航。Saleor 永远放在原理和实验之后。

## 章节

| 目录 | 内容 | 当前状态 |
|---|---|---|
| `00-Computer` | 进程、线程、协程、I/O | 第一批完整 |
| `01-Web` | HTTP 字节到业务函数 | 第一批完整 |
| `02-Database` | Page、Buffer Pool、B+Tree、索引、Planner | 第一批完整 |
| `03-Redis` | Cache Aside、一致性、Redis | 演化底稿 + 路线骨架 |
| `04-Message-Queue` | ACK、重试、DLQ、Kafka | 演化底稿 + 路线骨架 |
| `05-Distributed-Systems` | 幂等、超时、重试、背压、CAP | 演化底稿 + 路线骨架 |
| `06-Transaction-Systems` | 订单、库存、支付、Saga、Outbox | 演化底稿 + 路线骨架 |
| `07-Testing-Observability` | 测试、Log/Metric/Trace、性能 | 演化底稿 + 路线骨架 |
| `08-Deployment` | Docker、CI/CD、Kubernetes、恢复 | 演化底稿 + 路线骨架 |
| `09-Saleor-Case-Study` | 生产源码案例 | 架构演化底稿 |
| `10-Interview` | 分类面试与项目表达 | 路线骨架 |

## 快速开始

```bash
cd '/Volumes/undo 4t/git/learnA/面试八股/Backend-Engineer-from-Scratch'
source scripts/activate_lab.sh
python scripts/verify_environment.py
python scripts/run_all_tests.py

python 00-Computer/01-process_thread_coroutine.py
python 01-Web/01-http_message.py
python 02-Database/04-bplus_tree.py
```

第一次准备 Python 环境：

```bash
scripts/prepare_environment.sh
```

该脚本同时生成公开安全的确定性学习数据。数据说明见
[dataset/README.md](dataset/README.md)，输出位于 `.lab/learning-data/`。

PostgreSQL / Redis 实验：

```bash
# 先确保 Docker Desktop 已显示 Ready
scripts/finalize_environment.sh
```

执行计划和 Redis seed 回执保存在 `.lab/results/`。Redis 数据统一使用
`backend-lab:` 前缀，初始化脚本不会执行 `FLUSHDB`。

`activate_lab.sh` 会把 `.venv/bin` 和 Homebrew `libpq` 加入当前终端的
`PATH`，不会修改全局 `~/.zshrc`。数据库账号只用于本地教学容器。

`docker-compose.yml` 也已预留 RabbitMQ 4 + Management UI（AMQP
`localhost:55672`、UI `http://localhost:15673`），但当前第一批环境脚本不会自动启动它；
进入 MQ 章节后再显式运行 `docker compose up -d rabbitmq`。

## Visual Lab

开源器材、许可证和章节映射统一记录在 [VISUAL_TOOLS.md](VISUAL_TOOLS.md)。教材只链接和编写观察任务，不复制第三方代码。

当前第一批包括：

- 本地离线 Event Loop 动画。
- Wireshark HTTP/TCP 抓包任务。
- Chalmers B/B+Tree 交互动画。
- PEV2 PostgreSQL 执行计划树。

## 学习方式

见 [STUDY_GUIDE.md](STUDY_GUIDE.md)，提问模板见 [QUESTION_TEMPLATE.md](QUESTION_TEMPLATE.md)，进度见 [PROGRESS.md](PROGRESS.md)，权威资料见 [SOURCE_INDEX.md](SOURCE_INDEX.md)，Saleor 证据见 [SALEOR_SOURCE_INDEX.md](SALEOR_SOURCE_INDEX.md)。
