from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass
class Message:
    event_id: str
    order_id: str
    attempt: int = 0


class Broker:
    def __init__(self) -> None:
        self.ready: deque[Message] = deque()

    def publish(self, message: Message) -> None:
        self.ready.append(message)

    def redeliver(self, message: Message) -> None:
        message.attempt += 1
        self.ready.appendleft(message)


def consume_once(broker: Broker, processed: set[str], side_effects: list[str], fail_after_effect: bool) -> None:
    message = broker.ready.popleft()
    if message.event_id in processed:
        print("duplicate ignored:", message.event_id)
        return

    side_effects.append(f"email:{message.order_id}")
    if fail_after_effect:
        print("consumer crashed before ACK")
        broker.redeliver(message)
        return

    processed.add(message.event_id)
    print("ACK", message.event_id)


def main() -> None:
    broker = Broker()
    broker.publish(Message(event_id="evt-1", order_id="order-7"))
    processed: set[str] = set()
    side_effects: list[str] = []

    consume_once(broker, processed, side_effects, fail_after_effect=True)
    consume_once(broker, processed, side_effects, fail_after_effect=False)
    print("side effects:", side_effects)
    print("notice: ACK/retry alone cannot undo the first side effect")

    assert len(side_effects) == 2


if __name__ == "__main__":
    main()
