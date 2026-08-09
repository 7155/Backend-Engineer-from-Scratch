#!/usr/bin/env bash
set -euo pipefail

backend_lab_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export UV_CACHE_DIR="$backend_lab_root/.lab/uv-cache"
mkdir -p "$UV_CACHE_DIR"

python_candidate="/usr/local/bin/python3.12"
if [ ! -x "$python_candidate" ]; then
  python_candidate="$(command -v python3)"
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "ERROR: 缺少 uv。" >&2
  exit 1
fi

cd "$backend_lab_root"
uv sync --locked --python "$python_candidate"

for tool in psql pg_isready createdb dropdb; do
  target="/opt/homebrew/opt/libpq/bin/$tool"
  if [ -x "$target" ] && [ ! -e ".venv/bin/$tool" ]; then
    ln -s "$target" ".venv/bin/$tool"
  fi
done

.venv/bin/python scripts/prepare_learning_data.py
.venv/bin/python scripts/verify_environment.py

echo
echo "Python and learning data are ready."
echo "When Docker is accessible, run: scripts/finalize_environment.sh"
