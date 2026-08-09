#!/usr/bin/env bash
set -euo pipefail

backend_lab_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: 未找到 docker CLI。" >&2
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "ERROR: Docker daemon 尚未运行。" >&2
  echo "请先在 Finder 打开：/Volumes/undo 4t/Docker.app" >&2
  echo "看到 Docker Ready 后，再运行 scripts/start_services.sh。" >&2
  exit 2
fi

docker compose --project-directory "$backend_lab_root" up -d --wait postgres redis
docker compose --project-directory "$backend_lab_root" ps
