# 08 - 部署演化：脚本为什么会走到 Kubernetes

```text
V0 手工运行进程
→ 环境不一致、重启靠人
→ V1 Docker
→ 单机故障仍停服
→ V2 多实例 + Load Balancer
→ 发布、探活和调度复杂
→ V3 Orchestrator / Kubernetes
→ 平台本身复杂
→ CI/CD、SLO、容量与灾备治理
```

## 为什么手工部署曾经合理

一个内部服务、单台机器、可接受短暂停机时，systemd/进程管理器已经能解决重启。容器和 Kubernetes 不会减少业务 bug。

## 每次升级的代价

- Docker 固化环境，但引入镜像供应链、网络和存储边界。
- 多实例提高容量和可用性，却要求 stateless、共享存储和 graceful shutdown。
- Kubernetes提供调度与自愈，却增加 YAML、控制面、权限、探针和排障层级。
- Readiness 避免未就绪流量；错误探针也可能制造重启风暴。

Saleor `3.23.25` 的 `AGENTS.md` 明确假设多 Kubernetes Pod，因此位于 V3；这是目标部署模型，不代表每个小型 Saleor 开发环境都必须运行集群。Spring Boot 对应 Docker image、Actuator probes、Deployment/Service/HPA。

## 为什么创业项目不第一天拆 50 个 Pod

单实例尚未达到容量和恢复目标时，平台复杂度会超过业务收益。先量化 RTO、RPO、峰值负载和团队值班能力。

费曼题：Kubernetes 能重启崩溃 Pod，为什么仍不能替代数据库备份、幂等和 graceful shutdown？

## Sources

- [《凤凰架构》以容器构建系统](https://icyfenix.cn/immutable-infrastructure/container/container-build-system.html)
- [Kubernetes Concepts](https://kubernetes.io/docs/concepts/)
- [Kubernetes Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
