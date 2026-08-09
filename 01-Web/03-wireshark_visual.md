# 03 Visual Lab：Wireshark 看 TCP / HTTP

工具：[Wireshark 官网](https://www.wireshark.org/)；源码采用 GPL-2.0，GitHub 仓库是只读镜像。只抓取你有权限观察的本机教学流量。

## 输入什么

终端 A：

```bash
python3 01-Web/02-tiny_http_server.py --serve --port 8080
```

终端 B：

```bash
curl --http1.1 -v http://127.0.0.1:8080/health
```

若 macOS loopback 抓不到，选择 `Loopback: lo0`；显示过滤器输入：

```text
tcp.port == 8080
```

## 点击 / 执行什么

1. 开始抓包后再运行 curl。
2. 按时间查看 SYN、SYN-ACK、ACK。
3. 选中携带 `GET /health` 的包，展开 TCP 和 HTTP。
4. 右键该连接，选择 Follow → TCP Stream。
5. 重新运行一次，把客户端改为分段发送，观察一个 HTTP message 是否可跨多个 TCP segment。

## 观察什么

- 建立连接的三个握手包与双方 sequence/acknowledgment。
- HTTP 请求行和 Header 是 TCP payload，不是独立网络层消息。
- `Content-Length` 描述 HTTP Body 长度，不描述 TCP 包数量。
- 本实验响应包含 `Connection: close`，因此请求后会看到连接关闭过程。

## 为什么会这样

TCP 只提供可靠、有序字节流。分段由发送缓冲、MSS、网络和系统决定；HTTP parser 必须按自己的 Header/Body 规则重新组装。一次 `send`、一个 TCP segment、一次 `recv`、一条 HTTP request 不是一一对应关系。

## 费曼问题

> 抓包看到 Body 分在两个 TCP segment 中，为什么应用仍能得到一个完整 Request？反过来，为什么看到一个 segment 也不能证明一次 recv 就拿到全部字节？
