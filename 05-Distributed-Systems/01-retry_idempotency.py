from __future__ import annotations


class PaymentService:
    def __init__(self) -> None:
        self.charges: list[str] = []
        self.results: dict[str, str] = {}
        self.first_response_lost = True

    def charge_without_key(self, order_id: str) -> str:
        self.charges.append(order_id)
        if self.first_response_lost:
            self.first_response_lost = False
            raise TimeoutError("response lost after charge")
        return "ok"

    def charge_with_key(self, order_id: str, idempotency_key: str) -> str:
        if idempotency_key in self.results:
            return self.results[idempotency_key]
        self.charges.append(order_id)
        self.results[idempotency_key] = "ok"
        if self.first_response_lost:
            self.first_response_lost = False
            raise TimeoutError("response lost after charge")
        return "ok"


def retry(call):
    try:
        return call()
    except TimeoutError as exc:
        print("timeout -> retry:", exc)
        return call()


def main() -> None:
    unsafe = PaymentService()
    retry(lambda: unsafe.charge_without_key("order-1"))
    print("without idempotency:", unsafe.charges)

    safe = PaymentService()
    retry(lambda: safe.charge_with_key("order-2", "pay-order-2-v1"))
    print("with idempotency:", safe.charges)

    assert unsafe.charges == ["order-1", "order-1"]
    assert safe.charges == ["order-2"]


if __name__ == "__main__":
    main()
