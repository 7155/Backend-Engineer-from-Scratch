from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    "03-Redis/01-cache_aside.py",
    "04-Message-Queue/01-at_least_once.py",
    "05-Distributed-Systems/01-retry_idempotency.py",
    "06-Transaction-Systems/01-overselling_and_lock.py",
    "07-Testing-Observability/01-trace_pipeline.py",
    "08-Deployment/01-readiness_graceful_shutdown.py",
    "10-Practice/01-tinycommerce_capstone.py",
]


def main() -> None:
    for relative in SCRIPTS:
        print(f"\n=== {relative} ===")
        subprocess.run([sys.executable, str(ROOT / relative)], check=True)
    print("\nall v3.1 stdlib labs passed")


if __name__ == "__main__":
    main()
