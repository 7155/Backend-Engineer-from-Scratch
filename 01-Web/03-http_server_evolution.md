# 03 - Web 请求处理怎样从函数调用演化到 ASGI

## 最简单方案为什么合理

一个内部工具可以直接调用 Python 函数；只有当调用方跨进程、跨机器或使用不同语言时，才需要稳定的网络协议边界。

```text
V0 直接函数调用
→ V1 单连接 socket server
→ V2 HTTP message 与路由
→ V3 多线程/多进程 server
→ V4 WSGI 标准化 server 与 app 边界
→ V5 ASGI 支持 async 与长连接
→ V6 Load Balancer + 多 Pod
```

## 每次升级付出的代价

| 触发问题 | 优化 | 新问题 |
| --- | --- | --- |
| 调用方不在同一进程 | socket | 半包、粘连、超时、断连 |
| 每个项目重复造协议 | HTTP | Header/Body 限制、代理差异、安全解析 |
| 一个慢连接阻塞所有请求 | thread/process pool | worker 上限和排队 |
| Server 与框架强耦合 | WSGI | 同步调用模型不擅长长连接 |
| 大量 I/O 等待与 streaming | ASGI | 阻塞 ORM/SDK 会卡 Event Loop |
| 单实例容量与故障边界 | 多 Pod | 本地 session/锁失效，必须 stateless |

## 故障输入

`02-tiny_http_server.py` 故意把一个请求分成三次 `send`。Server 必须持续读取到 Header 结束和完整 `Content-Length`，说明网络边界出现后，业务函数不再能假设“一次调用就是完整输入”。

## 为什么小项目不直接多 Pod + ASGI

如果请求量低、没有 streaming，成熟的同步 Server 已经足够。多 Pod 会增加部署、日志聚合、幂等、共享 session、连接池预算和故障定位成本；ASGI 也不会自动把同步数据库调用变成非阻塞。

## Saleor 位于哪一层

Saleor `3.23.25` 的开发命令运行 `uvicorn saleor.asgi:application`；`saleor/graphql/views.py:GraphQLView.dispatch` 接收 Django 已解析的请求，`saleor/graphql/api.py` 构建 GraphQL schema。Socket、HTTP parser、GraphQL view 和业务 resolver 各有不同 owner。

## Java/Spring 对应

- WSGI 同类边界：Servlet API。
- ASGI/Event Loop：Spring WebFlux/Netty。
- 同步 worker：Tomcat thread pool。
- 多 Pod：无论 Django 还是 Spring，都必须把 session、锁和幂等状态放到共享边界。

## 费曼复述

为什么 Saleor 使用 ASGI/Uvicorn，仍不能证明一次 GraphQL 请求里的所有 ORM 和 Provider 调用都是非阻塞的？

## Sources

- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)
- [ASGI specification](https://asgi.readthedocs.io/en/latest/specs/main.html)
- [Python `socket`](https://docs.python.org/3/library/socket.html)
