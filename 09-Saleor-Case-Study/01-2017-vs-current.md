# 01 - 2017 与 3.23.25：约束变化，不是先进程度排名

## 比较样本

| 样本 | 版本证据 |
| --- | --- |
| 2017 | commit `7e57a29b9f0dd6e93ab77998b93b0d2fe37fcdd6`，2017-12-30 |
| 当前 | tag `3.23.25`，commit `bcb559a79ccafadb21bf9d337ef1dc6b74bd77a2` |

## 源码能直接证明的差异

| 维度 | 2017 样本 | 3.23.25 样本 |
| --- | --- | --- |
| 产品表述 | README：Python/Django e-commerce storefront | README：GraphQL native、API-only、headless |
| UI 边界 | 仓库内有 `saleor/dashboard/` 和 storefront/dashboard 静态资源 | README 指向独立 `saleor-dashboard` 仓库 |
| Web runtime | `requirements.txt` 有 uWSGI 2.0.15 | `pyproject.toml` 开发命令使用 Uvicorn + ASGI |
| Python/Django | Django 1.11.5 | Python 3.12；`uv.lock` 固定 Django 5.2.17 |
| 数据与异步依赖 | psycopg2、Redis 2.10、Celery 4.1、Elasticsearch 5 | psycopg 3、Redis client 5、Celery、OpenTelemetry 等 |
| 部署约束 | 本样本没有当前 `AGENTS.md` 的多 Pod 契约 | `AGENTS.md` 明确多 Pod、共享数据层、幂等和 `on_commit` |

## 能推断什么

从 UI 移出核心仓库、API-only 表述和多 Pod 契约，可以合理推断当前设计更重视客户端解耦、独立部署和水平扩展。

但这只是**架构差异推断**。没有 issue/PR 证据前，不能说某个客户规模、某次事故或某个团队重组是唯一原因。

## 为什么 2017 方案当时可能合理

- 一个仓库同时提供 storefront 与 dashboard，能减少跨仓库协议和发布协调。
- 同一 Django 应用内的模板、业务代码和事务边界更容易调试。
- 产品和团队边界尚未稳定时，拆分会提前固化接口。

## 当前方案获得与付出的东西

- 获得：不同客户端/扩展可独立技术选型、部署和扩容。
- 付出：网络部分失败、API 兼容、鉴权、Webhook 重试、跨仓库联调和可观测性成本。

## 复现实证

```bash
git -C .references/saleor show \
  7e57a29b9f0dd6e93ab77998b93b0d2fe37fcdd6:README.md
git -C .references/saleor show \
  7e57a29b9f0dd6e93ab77998b93b0d2fe37fcdd6:requirements.txt
git -C .references/saleor show 3.23.25:README.md
git -C .references/saleor show 3.23.25:pyproject.toml
```

## 费曼复述

为什么“Dashboard 从核心仓库拆出去”不能简单总结成新版更先进？请分别说出一个收益和一个新增成本。
