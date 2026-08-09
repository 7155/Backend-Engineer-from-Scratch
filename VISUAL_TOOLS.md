# 开源可视化器材

核验日期：`2026-08-09`。教材只链接这些工具并给观察任务，不复制第三方源码。若以后集成本地资源，必须固定版本、重新检查许可证并保留 attribution。

| 工具 | 用于观察 | 许可证/边界 | 计划章节 |
|---|---|---|---|
| [ChalmersGU Data Structure Visualizations](https://chalmersgu-data-structure-courses.github.io/visualization/) | B-Tree/B+Tree Insert、Delete、Find、split 和 root split | FreeBSD；官方页面建议优先链接最新页面 | `02-Database` |
| [PEV2](https://github.com/dalibo/pev2) | PostgreSQL 计划树、节点耗时、rows、loops | PostgreSQL License；官方提供离线单文件 `pev2.html` | `02-Database` |
| [Redis Commander](https://github.com/joeferner/redis-commander) | Key、Value、TTL、String/List/Set/ZSet/Stream | MIT；只连接本地教学 Redis，不接生产数据 | `03-Redis` |
| [RabbitMQ Management Plugin](https://www.rabbitmq.com/docs/management) | Queue length、ready/unacked、message rate、exchange/binding/channel | RabbitMQ 官方内置管理插件；UI 指标有采样间隔 | `04-Message-Queue` |
| [Kafbat UI](https://github.com/kafbat/kafka-ui) | Broker、Topic、Partition、Consumer Group、Lag、消息 | Apache-2.0；教学环境避免暴露敏感消息 | `04-Message-Queue` |
| [Wireshark](https://www.wireshark.org/) | TCP handshake、重传、HTTP Header、keep-alive | GPL-2.0；GitHub 是只读镜像，安装使用官网 | `01-Web` |
| [Jaeger](https://github.com/jaegertracing/jaeger) | Trace/Span 父子关系、关键路径、错误传播 | Apache-2.0 | `07-Testing-Observability` |
| [OpenTelemetry Demo](https://github.com/open-telemetry/opentelemetry-demo) | 近真实微服务链路和多语言 instrumentation | Apache-2.0；资源占用明显，后期再运行 | `07-Testing-Observability` |

## 选择顺序

1. 有成熟开源工具：写编号 `visual.md`，提供操作任务，不复制工具。
2. 工具太重：先给最小 Docker/离线运行路径，注明资源和权限。
3. 没有合适工具：写一个离线、自包含 `visual.html`，只展示当前概念。
4. 可视化输出不能代替源码、测试、执行计划或生产指标。

## 每份 Visual Lab 的固定内容

- 输入什么。
- 点击/执行什么。
- 观察哪个变化。
- 为什么会变化。
- 一个费曼复述题。
