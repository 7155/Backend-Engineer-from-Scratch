# Saleor 映射：一次 GraphQL 请求

固定参考 Saleor tag `3.23.25`，commit
`bcb559a79ccafadb21bf9d337ef1dc6b74bd77a2`。

```text
Uvicorn / ASGI
→ saleor/asgi.py application
→ saleor/urls.py
→ saleor/graphql/views.py GraphQLView.dispatch
→ handle_query / validation / execution
→ saleor/graphql/api.py schema
→ resolver / service / ORM
→ Django HttpResponse / ASGI response
```

已核验：

- `saleor/graphql/views.py` 的 `GraphQLView.dispatch` 区分 GET/POST，POST 进入查询处理。
- 同文件导入 `saleor/graphql/context.py` 的上下文函数，并记录请求、时长和 GraphQL query cost 等指标。
- `saleor/graphql/api.py` 组合 Query、Mutation 和 schema；它不负责 socket accept/recv。

本地追踪：

```bash
rg -n 'graphql|GraphQLView' .references/saleor/saleor/urls.py
rg -n 'class GraphQLView|def dispatch|def handle_query' .references/saleor/saleor/graphql/views.py
rg -n 'schema =|class Query|class Mutation' .references/saleor/saleor/graphql/api.py
```

故障追问：客户端断开时 resolver 是否继续？GraphQL HTTP 200 内的业务错误怎样计入指标？query cost 检查是否发生在数据库访问前？这些都要靠固定源码和运行测试验证。
