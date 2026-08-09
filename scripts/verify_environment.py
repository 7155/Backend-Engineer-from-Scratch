from __future__ import annotations

import argparse
import shutil
import socket
import subprocess
from pathlib import Path

REQUIRED_CHAPTERS = (
    "00-Computer",
    "01-Web",
    "02-Database",
    "03-Redis",
    "04-Message-Queue",
    "05-Distributed-Systems",
    "06-Transaction-Systems",
    "07-Testing-Observability",
    "08-Deployment",
    "09-Saleor-Case-Study",
    "10-Interview",
)

REQUIRED_ROOT_FILES = (
    "README.md",
    "STUDY_GUIDE.md",
    "PROGRESS.md",
    "ENGINEERING_EVOLUTION.md",
    "QUESTION_TEMPLATE.md",
    "SOURCE_INDEX.md",
    "SALEOR_REFERENCE.md",
    "SALEOR_SOURCE_INDEX.md",
    "VISUAL_TOOLS.md",
)

EVOLUTION_FILES = (
    "00-Computer/04-concurrency_evolution.md",
    "01-Web/03-http_server_evolution.md",
    "02-Database/07-index_evolution.md",
    "02-Database/12-transaction_evolution.md",
    "03-Redis/04-cache_evolution.md",
    "04-Message-Queue/07-message_queue_evolution.md",
    "05-Distributed-Systems/09-architecture_evolution.md",
    "06-Transaction-Systems/09-transaction_evolution.md",
    "07-Testing-Observability/06-observability_evolution.md",
    "08-Deployment/08-deployment_evolution.md",
)

SALEOR_CASE_FILES = (
    "09-Saleor-Case-Study/00-current-architecture.md",
    "09-Saleor-Case-Study/01-2017-vs-current.md",
    "09-Saleor-Case-Study/02-storefront-to-headless.md",
    "09-Saleor-Case-Study/03-single-app-to-multi-pod.md",
    "09-Saleor-Case-Study/04-architecture-tradeoffs.md",
)

FIRST_BATCH_FILES = (
    "00-Computer/01-process_thread_coroutine.py",
    "00-Computer/02-cpu_bound_vs_io_bound.py",
    "00-Computer/03-event_loop_visual.html",
    "00-Computer/04-concurrency_evolution.md",
    "00-Computer/90-saleor_mapping.md",
    "01-Web/01-http_message.py",
    "01-Web/02-tiny_http_server.py",
    "01-Web/03-http_server_evolution.md",
    "01-Web/04-wireshark_visual.md",
    "01-Web/90-saleor_mapping.md",
    "02-Database/01-page_io.py",
    "02-Database/02-buffer_pool.py",
    "02-Database/03-btree.py",
    "02-Database/04-bplus_tree.py",
    "02-Database/05-bplus_tree_visual.md",
    "02-Database/06-index_basic.sql",
    "02-Database/07-index_evolution.md",
    "02-Database/08-composite_index.sql",
    "02-Database/09-query_planner.py",
    "02-Database/10-explain_analyze.sql",
    "02-Database/11-explain_visual.md",
    "02-Database/12-transaction_evolution.md",
    "02-Database/90-saleor_mapping.md",
    "03-Redis/04-cache_evolution.md",
    "04-Message-Queue/07-message_queue_evolution.md",
    "05-Distributed-Systems/09-architecture_evolution.md",
    "06-Transaction-Systems/09-transaction_evolution.md",
    "07-Testing-Observability/06-observability_evolution.md",
    "08-Deployment/08-deployment_evolution.md",
)

LEGACY_CHAPTERS = (
    "00-computer-foundations",
    "01-web-request-lifecycle",
    "02-database-internals",
    "03-cache-and-redis",
    "04-message-queue-and-async",
    "05-concurrency-and-distributed-systems",
    "06-transaction-business-systems",
    "07-testing-observability-performance",
    "08-deployment-and-production",
    "10-interview-guide",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--require-services",
        action="store_true",
        help="同时要求 PostgreSQL 和 Redis 容器正在运行",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []

    for chapter in REQUIRED_CHAPTERS:
        readme = root / chapter / "README.md"
        if not readme.is_file():
            errors.append(f"缺少 {chapter}/README.md")

    for relative in REQUIRED_ROOT_FILES:
        if not (root / relative).is_file():
            errors.append(f"缺少根级教材文件 {relative}")

    for relative in FIRST_BATCH_FILES:
        if not (root / relative).is_file():
            errors.append(f"第一批缺少 {relative}")

    for relative in EVOLUTION_FILES:
        path = root / relative
        if not path.is_file():
            errors.append(f"缺少 Engineering Evolution 文件 {relative}")
            continue
        lesson = path.read_text(encoding="utf-8")
        for marker in ("## Sources", "费曼"):
            if marker not in lesson:
                errors.append(f"{relative} 缺少 {marker}")

    for relative in SALEOR_CASE_FILES:
        if not (root / relative).is_file():
            errors.append(f"缺少 Saleor 架构演化案例 {relative}")

    old_dirs = [root / name for name in LEGACY_CHAPTERS if (root / name).exists()]
    if old_dirs:
        errors.append("仍存在旧式小节目录布局")

    venv_python = root / ".venv" / "bin" / "python"
    if venv_python.is_file():
        venv_version = subprocess.run(
            [str(venv_python), "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        print(f"Virtualenv: {venv_version.stdout.strip()}")
    else:
        errors.append("缺少 .venv；运行 uv sync --python /usr/local/bin/python3.12")

    psql = shutil.which("psql") or "/opt/homebrew/opt/libpq/bin/psql"
    if Path(psql).is_file():
        psql_version = subprocess.run(
            [psql, "--version"], capture_output=True, text=True, check=False
        )
        print(f"PostgreSQL client: {psql_version.stdout.strip()}")
    else:
        errors.append("缺少 psql 客户端")

    learning_manifest = root / ".lab" / "learning-data" / "manifest.json"
    if learning_manifest.is_file():
        print("Learning data: prepared")
    else:
        errors.append("缺少学习数据；运行 python scripts/prepare_learning_data.py")

    pg_isready = root / ".venv" / "bin" / "pg_isready"
    postgres_ready = False
    if pg_isready.is_file():
        postgres_ready = (
            subprocess.run(
                [
                    str(pg_isready),
                    "-h",
                    "127.0.0.1",
                    "-p",
                    "55432",
                    "-U",
                    "backend_lab",
                    "-d",
                    "backend_lab",
                ],
                capture_output=True,
                text=True,
                check=False,
            ).returncode
            == 0
        )
    print(f"PostgreSQL service: {'ready' if postgres_ready else 'not reachable'}")

    try:
        with socket.create_connection(("127.0.0.1", 56379), timeout=0.5) as connection:
            connection.sendall(b"*1\r\n$4\r\nPING\r\n")
            redis_ready = connection.recv(32).startswith(b"+PONG")
    except OSError:
        redis_ready = False
    print(f"Redis service: {'ready' if redis_ready else 'not reachable'}")

    docker = shutil.which("docker")
    if docker is None:
        print("Docker: 未安装（SQL 扩展实验可稍后运行）")
    else:
        probe = subprocess.run(
            [docker, "version", "--format", "{{.Server.Version}}"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if probe.returncode == 0:
            print(f"Docker: daemon {probe.stdout.strip()}")
        else:
            print("Docker: client 已安装，daemon 当前不可用（SQL 尚不能实跑）")

    if args.require_services:
        if not postgres_ready:
            errors.append("PostgreSQL 服务未就绪：127.0.0.1:55432")
        if not redis_ready:
            errors.append("Redis 服务未就绪：127.0.0.1:56379")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Juliepy-style chapter structure: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
