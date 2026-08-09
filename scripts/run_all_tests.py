from __future__ import annotations

import importlib.util
import sys
import traceback
from pathlib import Path


def load_module(path: Path, index: int):
    spec = importlib.util.spec_from_file_location(f"lesson_{index}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载 {path}")
    module = importlib.util.module_from_spec(spec)
    # dataclass 等标准库会在定义类时通过 sys.modules 查找当前模块。
    # 手工 exec_module 前先注册，行为才和普通 import 一致。
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    lessons = sorted(root.glob("0[0-2]-*/[0-9][0-9]-*.py"))
    failures = 0
    for index, lesson in enumerate(lessons):
        relative = lesson.relative_to(root)
        try:
            module = load_module(lesson, index)
            self_check = module.self_check
            self_check()
            print(f"PASS {relative}")
        except Exception:
            failures += 1
            print(f"FAIL {relative}")
            traceback.print_exc()
    print(f"Checked {len(lessons)} Python lessons; failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
