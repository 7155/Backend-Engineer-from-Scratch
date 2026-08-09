# 06 Transaction Business Systems

> 状态：路线骨架，第二重点章。

围绕：Cart → Checkout → Inventory Reservation → Order → Payment → Allocation → Fulfillment → Refund/Cancel → Webhook。

## 计划顺序

1. `01-order_state_machine.py`
2. `02-inventory_overselling.py`
3. `03-checkout_to_order.py`
4. `04-payment_authorize_capture_refund.py`
5. `05-payment_result_unknown.py`
6. `06-webhook_signature_replay.py`
7. `07-saga_compensation.py`
8. `08-transactional_outbox.py`
9. `09-transaction_evolution.md`：订单记录怎样演化成状态机、补偿和 Outbox。
10. `10-order_visual.html`：本地离线状态机与补偿动画。
11. `90-saleor_mapping.md`
