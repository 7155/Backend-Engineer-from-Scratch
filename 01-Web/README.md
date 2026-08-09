# 01 Web Request Lifecycle

目标：从原始 HTTP 字节走到请求对象、路由、业务函数和响应，并知道成熟 Server 替我们处理了什么。

## 学习顺序

1. `01-http_message.py`：请求行、Header、Body 边界和响应编码。
2. `02-tiny_http_server.py`：socket accept/recv/sendall；默认只跑本地 socketpair，不占端口。
3. `03-http_server_evolution.md`：函数调用怎样演化到 HTTP、WSGI、ASGI 和多 Pod。
4. `04-wireshark_visual.md`：真实抓取 TCP handshake 与 HTTP 请求。
5. `90-saleor_mapping.md`：Uvicorn/ASGI → Django URL → GraphQLView → schema。

运行：

```bash
python3 01-Web/01-http_message.py
python3 01-Web/02-tiny_http_server.py
python3 01-Web/02-tiny_http_server.py --serve --port 8080
```

## 国内面试关键词

TCP 字节流、粘包/拆包、Content-Length、keep-alive、WSGI/ASGI、请求超时、反向代理、Slowloris、请求走私。

## 费曼复述

> 一个 POST 请求分三次到达：半个 Header、剩余 Header 加 `he`、最后 `llo`。Server 靠什么判断何时才能调用业务函数？生产还必须加哪三个限制？
