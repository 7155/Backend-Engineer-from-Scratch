# Saleor 映射：在线请求与后台任务

固定参考 Saleor tag `3.23.25`，commit
`bcb559a79ccafadb21bf9d337ef1dc6b74bd77a2`。路径和 symbol 已在本地只读
checkout 核验；行号只用于当前版本，不跨版本引用。

## 在线 API

```text
Uvicorn
→ saleor/asgi.py application
→ Django middleware / URL
→ saleor/graphql/views.py GraphQLView
→ resolver / service / ORM
```

官方 `pyproject.toml` 的开发命令使用 `uvicorn saleor.asgi:application --reload`。这里的关键不是“Saleor 用了协程所以全异步”，而是检查每个 ORM/SDK 调用是否会占住当前请求 worker，以及数据库连接池上限。

## 后台任务

```text
API 发布任务
→ broker
→ celery --app saleor.celeryconf:app worker
→ 各模块 tasks.py
```

Celery worker 是独立运行入口。请求超时、任务投递成功、任务执行成功是三个状态；重试必须配幂等和可观测终态。

## 本地追踪

```bash
rg -n 'uvicorn|celery --app' .references/saleor/pyproject.toml
rg -n 'class GraphQLView|def dispatch' .references/saleor/saleor/graphql/views.py
rg -n '@.*task|shared_task' .references/saleor/saleor -g 'tasks.py'
```

## 面试边界

源码能证明运行入口与调用关系，不能单独证明生产 worker 数、阻塞时间、连接池容量或用户可见延迟；这些需要部署配置和运行指标。
