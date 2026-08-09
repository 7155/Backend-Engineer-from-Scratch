# Saleor 参考规则

- 官方仓库：`https://github.com/saleor/saleor`
- 初始网页核验：`main`，`2026-08-09`
- 已核验路径：`saleor/graphql/api.py`、`saleor/graphql/views.py`、`saleor/urls.py`、`saleor/checkout/models.py`、`saleor/celeryconf.py`
- `main` 会变化；函数级学习前必须固定 tag/commit。

```bash
git clone --filter=blob:none https://github.com/saleor/saleor.git .references/saleor
git -C .references/saleor switch --detach <tag-or-commit>
git -C .references/saleor rev-parse HEAD
```

记录格式：

```text
参考版本：tag + commit
API 入口：path:function
业务函数：path:function
模型/索引：path:symbol
事务/锁：path:function
异步事件：path:task
测试：path:test
已验证：命令或源码事实
未验证：运行时与生产边界
```
