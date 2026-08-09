"""
01 - HTTP Message：框架 Request 之前，只是一段有边界规则的字节。

具体输入：
POST /echo HTTP/1.1\r\n
Content-Length: 5\r\n
\r\n
hello

执行顺序：请求行 → Header → 空行 → 按 Content-Length 读取 Body → 路由 → 响应编码。
本文件故意不处理 chunked、keep-alive、TLS、HTTP/2；它是协议边界实验，不是生产 Server。

运行：
  python3 01-Web/01-http_message.py
  python3 01-Web/01-http_message.py --request-file .lab/learning-data/http/02-echo.http
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from http import HTTPStatus
from pathlib import Path


@dataclass(frozen=True)
class Request:
    method: str
    path: str
    version: str
    headers: dict[str, str]
    body: bytes


@dataclass(frozen=True)
class Response:
    status: HTTPStatus
    body: bytes
    headers: dict[str, str] = field(default_factory=dict)

    def to_bytes(self) -> bytes:
        # 状态行和 Header 使用 CRLF；空行之后才是原始 Body。
        headers = {
            "Content-Length": str(len(self.body)),
            "Connection": "close",
            **self.headers,
        }
        lines = [f"HTTP/1.1 {self.status.value} {self.status.phrase}"]
        lines.extend(f"{name}: {value}" for name, value in headers.items())
        return ("\r\n".join(lines) + "\r\n\r\n").encode("ascii") + self.body


class BadRequest(ValueError):
    pass


def parse_request(raw: bytes) -> Request:
    try:
        raw_head, body = raw.split(b"\r\n\r\n", 1)
        lines = raw_head.decode("iso-8859-1").split("\r\n")
        method, path, version = lines[0].split(" ", 2)
    except (ValueError, UnicodeDecodeError) as error:
        raise BadRequest("malformed request line or headers") from error

    headers: dict[str, str] = {}
    for line in lines[1:]:
        if ":" not in line:
            raise BadRequest(f"malformed header: {line!r}")
        name, value = line.split(":", 1)
        headers[name.strip().lower()] = value.strip()

    try:
        content_length = int(headers.get("content-length", "0"))
    except ValueError as error:
        raise BadRequest("Content-Length must be an integer") from error
    if content_length < 0:
        raise BadRequest("Content-Length cannot be negative")
    if len(body) < content_length:
        raise BadRequest("request body is incomplete")

    return Request(method, path, version, headers, body[:content_length])


def route(request: Request) -> Response:
    if request.method == "GET" and request.path == "/health":
        body = json.dumps({"status": "ok"}).encode()
        return Response(HTTPStatus.OK, body, {"Content-Type": "application/json"})
    if request.method == "POST" and request.path == "/echo":
        content_type = request.headers.get("content-type", "application/octet-stream")
        return Response(HTTPStatus.OK, request.body, {"Content-Type": content_type})
    return Response(HTTPStatus.NOT_FOUND, b"not found", {"Content-Type": "text/plain"})


def handle_raw_request(raw: bytes) -> bytes:
    try:
        return route(parse_request(raw)).to_bytes()
    except BadRequest as error:
        return Response(
            HTTPStatus.BAD_REQUEST,
            str(error).encode(),
            {"Content-Type": "text/plain"},
        ).to_bytes()


def self_check() -> None:
    raw = b"POST /echo HTTP/1.1\r\nContent-Length: 5\r\nX-ID: 42\r\n\r\nhello"
    request = parse_request(raw)
    assert (request.method, request.path, request.body) == ("POST", "/echo", b"hello")
    assert request.headers["x-id"] == "42"
    response = handle_raw_request(b"GET /health HTTP/1.1\r\n\r\n")
    head, body = response.split(b"\r\n\r\n", 1)
    assert response.startswith(b"HTTP/1.1 200 OK")
    assert f"Content-Length: {len(body)}".encode() in head


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-file", type=Path)
    args = parser.parse_args()
    raw = (
        args.request_file.read_bytes()
        if args.request_file
        else b"GET /health HTTP/1.1\r\nHost: localhost\r\n\r\n"
    )
    request = parse_request(raw)
    print(f"parsed: method={request.method} path={request.path} headers={request.headers}")
    print(handle_raw_request(raw).decode())


if __name__ == "__main__":
    self_check()
    main()


# 生产故障
# --------
# - TCP 没有消息边界：一次 recv 可能只有半个 Header，也可能包含多个 write 的数据。
# - 不限制 Header/Body 大小和读取时间，会被慢连接或超大请求耗尽资源。
# - 代理与后端若对 Content-Length / Transfer-Encoding 理解不同，可能产生请求走私。
#
# 面试追问
# --------
# 客户端超时不等于服务端写入失败；写操作可能已提交、仍在执行或确实失败，
# 所以重试接口需要幂等键和结果查询。
#
# 费曼问题
# --------
# 为什么 `len(body) < Content-Length` 时不能先把现有字节交给业务函数？
