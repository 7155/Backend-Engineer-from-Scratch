from __future__ import annotations


class Service:
    def __init__(self) -> None:
        self.ready = False
        self.draining = False
        self.inflight = 0

    def start(self) -> None:
        self.ready = True

    def accept(self) -> bool:
        if not self.ready or self.draining:
            return False
        self.inflight += 1
        return True

    def finish(self) -> None:
        self.inflight -= 1

    def begin_shutdown(self) -> None:
        self.draining = True
        self.ready = False


def main() -> None:
    service = Service()
    print("before start ready=", service.ready)
    service.start()
    assert service.accept()
    print("request accepted; inflight=", service.inflight)

    service.begin_shutdown()
    print("draining; ready=", service.ready)
    print("new request accepted?", service.accept())
    service.finish()
    print("old request finished; inflight=", service.inflight)
    assert service.inflight == 0


if __name__ == "__main__":
    main()
