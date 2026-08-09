"""生成公开安全、确定性的第一批学习数据。

数据写到 .lab/learning-data，因此可以随时删除重建，不进入 Git。

运行：
  python scripts/prepare_learning_data.py
  python scripts/prepare_learning_data.py --check
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

SEED = 20_260_809
ORDER_ROWS = 1_000
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / ".lab" / "learning-data"


def http_request(method: str, path: str, body: bytes = b"", content_type: str = "") -> bytes:
    headers = [f"{method} {path} HTTP/1.1", "Host: 127.0.0.1:8080"]
    if body:
        headers.append(f"Content-Length: {len(body)}")
    if content_type:
        headers.append(f"Content-Type: {content_type}")
    headers.append("Connection: close")
    return "\r\n".join(headers).encode("ascii") + b"\r\n\r\n" + body


def orders_csv() -> bytes:
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(("id", "user_id", "status", "created_at", "total_cents"))

    statuses = ("NEW", "PAID", "SHIPPED", "CANCELLED")
    started = datetime(2025, 1, 1, tzinfo=UTC)
    for order_id in range(1, ORDER_ROWS + 1):
        writer.writerow(
            (
                order_id,
                order_id % 100,
                # 同一 user_id 跨轮次拥有不同状态，避免两列形成伪相关。
                statuses[(order_id // 100) % len(statuses)],
                (started + timedelta(seconds=order_id * 17)).isoformat(),
                1_000 + (order_id * 137) % 100_000,
            )
        )
    return output.getvalue().encode("utf-8")


def query_cases() -> bytes:
    cases = [
        {
            "name": "leftmost_column",
            "where": "user_id = 17",
            "predict": "can narrow by the first index column",
        },
        {
            "name": "two_column_prefix",
            "where": "user_id = 17 AND status = 'PAID'",
            "predict": "can narrow by user_id then status",
        },
        {
            "name": "skip_leftmost",
            "where": "status = 'PAID'",
            "predict": "cannot directly seek one continuous user_id prefix",
        },
        {
            "name": "prefix_then_range",
            "where": "user_id = 17 AND status = 'PAID' AND created_at >= '2025-01-01'",
            "predict": "equality prefix followed by a created_at range",
        },
        {
            "name": "range_then_filter",
            "where": "user_id > 90 AND status = 'PAID'",
            "predict": "status is commonly a filter after the user_id range",
        },
    ]
    return (json.dumps(cases, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def expected_files() -> dict[str, bytes]:
    return {
        "http/01-health.http": http_request("GET", "/health"),
        "http/02-echo.http": http_request("POST", "/echo", b"hello", "text/plain"),
        "http/03-json.http": http_request(
            "POST", "/echo", b'{"lesson":"backend"}', "application/json"
        ),
        "database/orders_small.csv": orders_csv(),
        "database/query_cases.json": query_cases(),
    }


def manifest(files: dict[str, bytes]) -> bytes:
    payload = {
        "format_version": 1,
        "seed": SEED,
        "orders_rows": ORDER_ROWS,
        "files": {
            name: {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}
            for name, content in sorted(files.items())
        },
    }
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write_data() -> None:
    files = expected_files()
    files["manifest.json"] = manifest(files)
    for relative, content in files.items():
        destination = OUTPUT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
    print(f"Prepared {len(files)} files in {OUTPUT}")


def check_data() -> None:
    files = expected_files()
    files["manifest.json"] = manifest(files)
    mismatches: list[str] = []
    for relative, expected in files.items():
        destination = OUTPUT / relative
        if not destination.is_file() or destination.read_bytes() != expected:
            mismatches.append(relative)
    if mismatches:
        raise SystemExit("Learning data mismatch: " + ", ".join(mismatches))
    print(f"Learning data check passed: {len(files)} files, {ORDER_ROWS} order rows")


def self_check() -> None:
    health = http_request("GET", "/health")
    echo = http_request("POST", "/echo", b"hello", "text/plain")
    assert health.endswith(b"\r\n\r\n")
    assert b"Content-Length: 5\r\n" in echo
    assert orders_csv().count(b"\n") == ORDER_ROWS + 1
    assert len(json.loads(query_cases())) == 5


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    self_check()
    if args.check:
        check_data()
    else:
        write_data()


if __name__ == "__main__":
    main()
