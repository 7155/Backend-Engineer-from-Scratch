"""
02 - Tiny HTTP Server：把上一文件的“消息解析”接到真实 socket。

默认模式使用 socketpair 在本进程模拟 client/server，不占端口、不会等待。
传 --serve 时才监听一个真实 TCP 连接，处理完成后退出。

运行：
  python3 01-Web/02-tiny_http_server.py
  python3 01-Web/02-tiny_http_server.py --serve --port 8080
"""

from __future__ import annotations

import argparse
import runpy
import socket
from pathlib import Path

# 编号学习文件带短横线，不能用普通 import 语句；run_path 复用上一节的实现，
# 同时避免把解析代码复制一遍。它不会执行上一节的 __main__ 分支。
HTTP = runpy.run_path(str(Path(__file__).with_name("01-http_message.py")))
handle_raw_request = HTTP["handle_raw_request"]


def receive_one_request(connection: socket.socket) -> bytes:
    data = bytearray()
    header_end: int | None = None
    content_length = 0

    while True:
        chunk = connection.recv(4096)
        if not chunk:
            break
        data.extend(chunk)

        # TCP 只给字节；应用必须自己寻找 HTTP Header 边界。
        if header_end is None and b"\r\n\r\n" in data:
            header_end = data.index(b"\r\n\r\n") + 4
            header_text = data[:header_end].decode("iso-8859-1")
            for line in header_text.split("\r\n"):
                if line.lower().startswith("content-length:"):
                    content_length = int(line.split(":", 1)[1].strip())

        if header_end is not None and len(data) >= header_end + content_length:
            break

    return bytes(data)


def serve_connection(connection: socket.socket) -> None:
    raw = receive_one_request(connection)
    connection.sendall(handle_raw_request(raw))


def serve_once(host: str = "127.0.0.1", port: int = 8080) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(1)
        print(f"listening once on http://{host}:{port}")
        connection, address = server.accept()  # 当前实验会阻塞等待一个连接
        with connection:
            print(f"accepted {address}")
            serve_connection(connection)


def socketpair_demo() -> bytes:
    server_side, client_side = socket.socketpair()
    try:
        # 故意分三次 send，证明服务端不能假设一次 recv 就是完整请求。
        client_side.sendall(b"POST /echo HTTP/1.1\r\nContent-Length: 5\r\n")
        client_side.sendall(b"Content-Type: text/plain\r\n\r\nhe")
        client_side.sendall(b"llo")
        serve_connection(server_side)
        return client_side.recv(4096)
    finally:
        server_side.close()
        client_side.close()


def self_check() -> None:
    response = socketpair_demo()
    assert response.startswith(b"HTTP/1.1 200 OK")
    assert response.endswith(b"hello")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    if args.serve:
        serve_once(port=args.port)
    else:
        print(socketpair_demo().decode())


if __name__ == "__main__":
    self_check()
    main()


# 生产边界
# --------
# 本实验没有 TLS、keep-alive、chunked、HTTP/2、并发、超时、大小限制、
# backpressure 和 graceful shutdown。不要把它部署到公网；成熟 Server 负责这些协议细节。
#
# 面试问题
# --------
# WSGI/ASGI 是 Server 调用 Python 应用的契约，不是 TCP 本身。Uvicorn 负责连接和
# HTTP 解析，Django/Saleor 接收结构化请求并运行 middleware、路由和业务代码。
