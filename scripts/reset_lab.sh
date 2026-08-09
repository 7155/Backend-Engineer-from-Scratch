#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "This removes Docker volumes created by this curriculum."
docker compose --project-directory "$repo_dir" down -v --remove-orphans
