#!/usr/bin/env bash
# 用法：source scripts/activate_lab.sh
# 只修改当前终端，不写入 ~/.zshrc 或其他机器级配置。

if [ -n "${ZSH_VERSION:-}" ]; then
  activate_lab_source="${(%):-%N}"
else
  activate_lab_source="${BASH_SOURCE[0]}"
fi

backend_lab_root="$(cd "$(dirname "$activate_lab_source")/.." && pwd)"

export BACKEND_LAB_ROOT="$backend_lab_root"
export UV_CACHE_DIR="$backend_lab_root/.lab/uv-cache"
export PATH="$backend_lab_root/.venv/bin:/opt/homebrew/opt/libpq/bin:$PATH"

mkdir -p "$UV_CACHE_DIR"

echo "Backend lab activated: $BACKEND_LAB_ROOT"
python --version
if command -v psql >/dev/null 2>&1; then
  psql --version
fi
