import psycopg2

from order_generator import generate_orders

connection = psycopg2.connect(
    host="localhost",
    database="enterprise_db",
    user="postgres",
    password="postgres"
)
cursor = connection.cursor()

orders = generate_orders()

cursor.executemany(
    """
    INSERT INTO orders
    (customer_id,
     product_id,
     quantity,
     order_date,
     amount,
     payment_method,
     order_status)

    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """,
    orders
)

connection.commit()

cursor.close()
connection.close()

print("1000 Orders Inserted Successfully!")