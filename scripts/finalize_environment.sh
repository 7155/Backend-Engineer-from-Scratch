#!/usr/bin/env bash
set -euo pipefail

backend_lab_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$backend_lab_root"

scripts/prepare_environment.sh
scripts/start_services.sh
scripts/run_database_labs.sh
scripts/seed_redis_lab.sh

source scripts/activate_lab.sh >/dev/null
python scripts/run_all_tests.py
python scripts/prepare_learning_data.py --check
python scripts/verify_environment.py --require-services

echo
echo "Backend learning environment is ready."
