from __future__ import annotations


def lost_update_demo() -> tuple[int, int]:
    stock = 1
    a_read = stock
    b_read = stock
    a_success = a_read > 0
    b_success = b_read > 0
    if a_success:
        stock = a_read - 1
    if b_success:
        stock = b_read - 1
    return stock, int(a_success) + int(b_success)


def serialized_demo() -> tuple[int, int]:
    stock = 1
    success = 0
    for _request in ("A", "B"):
        if stock <= 0:
            continue
        stock -= 1
        success += 1
    return stock, success


def main() -> None:
    stock, orders = lost_update_demo()
    print("without serialization: stock=", stock, "successful orders=", orders)
    locked_stock, locked_orders = serialized_demo()
    print("with serialized critical section: stock=", locked_stock, "successful orders=", locked_orders)
    assert (stock, orders) == (0, 2)
    assert (locked_stock, locked_orders) == (0, 1)


if __name__ == "__main__":
    main()
