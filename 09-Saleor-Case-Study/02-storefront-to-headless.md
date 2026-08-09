# 02 - Storefront 到 Headless/API-only

## V0：后端同时渲染 Storefront

同一团队交付一个 Web 商店时，Django 模板、管理页面和交易逻辑同仓库非常合理：函数调用快、部署单一、登录和数据模型边界直接。

## 触发演化的问题

当客户端出现 Web、移动端、POS、合作方和自定义 Dashboard 时，绑定一种 UI 发布节奏会限制独立迭代。扩展代码直接进入核心进程，也会共享故障与升级边界。

```text
内置 Storefront/Dashboard
→ 多客户端与独立发布需求
→ 稳定 GraphQL API
→ Dashboard / Storefront 独立部署
→ 第三方扩展跨网络
→ Webhook/App 的鉴权、重试、版本与可观测性
```

## 当前源码证据

- 2017 README 直接称 Saleor 为 storefront，历史树中存在 `saleor/dashboard/`。
- 3.23.25 README 明确写 API-only/headless，并链接独立 Dashboard 仓库。
- `saleor/graphql/views.py` 与 `saleor/graphql/api.py` 是当前 API 边界。

## 新方案的新问题

- 一次本地调用变成可能超时、重复或结果未知的网络调用。
- API schema 要承担兼容性和权限边界。
- UI 与后端不能再依赖同一次数据库事务发布。
- Webhook/App 扩展需要签名、重放保护、幂等和失败恢复。

## 什么时候不要这样拆

单一客户端、单团队、低流量且需要快速验证业务时，模块化单体和服务端渲染可能更便宜。Headless 解决的是客户端与组织边界，不会自动提高单次查询性能。

## Java/Spring 对应

Spring MVC + Thymeleaf 是内置 storefront 路线；Spring Boot GraphQL/REST + 独立前端是 headless 路线。底层权衡与语言无关。

## 费曼复述

为什么 Headless 能让 Storefront 独立发布，却同时把原本的函数异常变成了超时、重试和兼容性问题？
