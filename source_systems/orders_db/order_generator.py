import random
from datetime import datetime, timedelta


PAYMENT_METHODS = ["Credit Card", "UPI", "Debit Card", "Net Banking", "Cash"]

ORDER_STATUS = ["Pending", "Shipped", "Delivered", "Cancelled"]


def generate_orders(num_orders=1000):
    orders = []

    for _ in range(num_orders):
        order = (
            random.randint(1, 500),                      # customer_id
            random.randint(1, 200),                      # product_id
            random.randint(1, 5),                        # quantity
            datetime.now().date() - timedelta(days=random.randint(0, 365)),
            round(random.uniform(100, 10000), 2),       # amount
            random.choice(PAYMENT_METHODS),
            random.choice(ORDER_STATUS)
        )

        orders.append(order)

    return orders