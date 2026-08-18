from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Span:
    name: str
    duration_ms: int
    attributes: dict[str, str] = field(default_factory=dict)


def handle_checkout(request_id: str) -> list[Span]:
    spans = [
        Span("graphql.checkoutComplete", 12, {"request_id": request_id}),
        Span("db.lock_checkout", 8, {"request_id": request_id}),
        Span("db.create_order", 20, {"request_id": request_id}),
        Span("outbox.insert", 3, {"request_id": request_id}),
    ]
    return spans


def main() -> None:
    request_id = "req-42"
    spans = handle_checkout(request_id)
    total = sum(span.duration_ms for span in spans)
    print("trace", request_id)
    for span in spans:
        print(f"  {span.name:<28} {span.duration_ms:>3} ms")
    print("critical-path total:", total, "ms")
    slowest = max(spans, key=lambda item: item.duration_ms)
    print("slowest span:", slowest.name)
    assert slowest.name == "db.create_order"


if __name__ == "__main__":
    main()
