from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Entry:
    value: str
    expires_at: int


class TinyCache:
    def __init__(self) -> None:
        self.data: dict[str, Entry] = {}

    def get(self, key: str, now: int) -> str | None:
        item = self.data.get(key)
        if item is None:
            return None
        if item.expires_at <= now:
            del self.data[key]
            return None
        return item.value

    def set(self, key: str, value: str, ttl: int, now: int) -> None:
        self.data[key] = Entry(value=value, expires_at=now + ttl)

    def delete(self, key: str) -> None:
        self.data.pop(key, None)


def get_product(product_id: int, db: dict[int, str], cache: TinyCache, now: int) -> tuple[str, str]:
    key = f"product:{product_id}"
    cached = cache.get(key, now)
    if cached is not None:
        return cached, "cache-hit"
    value = db[product_id]
    cache.set(key, value, ttl=5, now=now)
    return value, "db-read"


def main() -> None:
    db = {1: "keyboard-v1"}
    cache = TinyCache()

    print("t=0", get_product(1, db, cache, now=0))
    print("t=1", get_product(1, db, cache, now=1))

    db[1] = "keyboard-v2"
    print("db updated, cache not invalidated")
    print("t=2", get_product(1, db, cache, now=2), "<- stale")

    cache.delete("product:1")
    print("cache invalidated")
    print("t=3", get_product(1, db, cache, now=3))

    assert get_product(1, db, cache, now=4)[0] == "keyboard-v2"


if __name__ == "__main__":
    main()
