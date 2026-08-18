from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Order:
    order_id: str
    status: str
    amount: int


class TinyCommerce:
    def __init__(self) -> None:
        self.stock = {"sku-1": 1}
        self.orders: dict[str, Order] = {}
        self.idempotency: dict[str, str] = {}
        self.outbox: list[tuple[str, str]] = []

    def checkout(self, checkout_id: str, idem_key: str) -> Order:
        if idem_key in self.idempotency:
            return self.orders[self.idempotency[idem_key]]

        if self.stock["sku-1"] <= 0:
            raise RuntimeError("sold out")

        self.stock["sku-1"] -= 1
        order_id = f"order-{len(self.orders) + 1}"
        order = Order(order_id=order_id, status="UNCONFIRMED", amount=100)
        self.orders[order_id] = order
        self.idempotency[idem_key] = order_id
        self.outbox.append(("ORDER_CREATED", order_id))
        return order

    def publish_outbox(self) -> list[str]:
        published = [f"{event}:{order_id}" for event, order_id in self.outbox]
        self.outbox.clear()
        return published


def main() -> None:
    app = TinyCommerce()
    first = app.checkout("checkout-7", "complete-checkout-7")
    retry = app.checkout("checkout-7", "complete-checkout-7")

    print("first:", first)
    print("retry returns same order:", retry)
    print("stock:", app.stock)
    print("outbox before publish:", app.outbox)
    print("published:", app.publish_outbox())

    assert first.order_id == retry.order_id
    assert app.stock["sku-1"] == 0
    assert len(app.orders) == 1


if __name__ == "__main__":
    main()
