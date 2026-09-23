import random
import uuid
from datetime import datetime, timezone

from faker import Faker
import pymysql
from pymongo import MongoClient

fake = Faker()

TOTAL_RECORDS = 20000
BATCH_SIZE = 2000

print("=" * 55)
print("🚀 POBLANDO BASES DE DATOS HARDTECHHUB")
print("=" * 55)

# ====================================================
# 1. MYSQL (hardtech_orders)
# ====================================================
print("\n=== 1. POBLANDO MYSQL (hardtech_orders) ===")

try:
    mysql_conn = pymysql.connect(
        host="localhost",
        port=3307,
        user="orders_app",
        password="orders2026",
        database="hardtech_orders",
        autocommit=False,
    )

    mysql_cur = mysql_conn.cursor()

    # ------------------------------------------------
    # ORDERS
    # ------------------------------------------------
    mysql_cur.execute("SELECT COUNT(*) FROM orders;")
    orders_count = mysql_cur.fetchone()[0]

    remaining_orders = TOTAL_RECORDS - orders_count

    if remaining_orders > 0:
        print(f"Insertando {remaining_orders} órdenes...")

        statuses = ["RESERVING", "PENDING", "PAID", "SHIPPED", "CANCELLED"]
        mysql_data = []

        for i in range(remaining_orders):
            status = random.choice(statuses)

            subtotal = round(random.uniform(30.0, 2500.0), 2)
            tax = round(subtotal * 0.18, 2)
            shipping = random.choice([0.0, 15.0, 25.0])
            total = round(subtotal + tax + shipping, 2)

            request_key = f"ORD-{uuid.uuid4().hex[:12]}"

            created = fake.date_time_between(
                start_date="-1y",
                end_date="now"
            ).strftime("%Y-%m-%d %H:%M:%S")

            mysql_data.append(
                (
                    status,
                    subtotal,
                    tax,
                    shipping,
                    total,
                    request_key,
                    created,
                )
            )

            if len(mysql_data) >= BATCH_SIZE:
                mysql_cur.executemany(
                    """
                    INSERT INTO orders
                    (status, subtotal, tax, shipping_cost, total_amount, request_key, created_at)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                    """,
                    mysql_data,
                )
                mysql_conn.commit()
                mysql_data.clear()



            "Procesadores",
            "Tarjetas Graficas",
            "Memorias RAM",
        ]
        items = []

        for order_id in order_ids:
            for _ in range(random.randint(1, 3)):
                product_id = random.randint(1, 100)
                quantity = random.randint(1, 4)
                unit_price = round(random.uniform(50.0, 800.0), 2)
                subtotal = round(quantity * unit_price, 2)

                items.append(
                    (
                        order_id,
                        product_id,
                        f"SKU-{product_id:06d}",
                        f"Componente {product_id}",
                        random.choice(categories),
                        quantity,

                        unit_price,
                        subtotal,
        categories = [
                    )
                )
        mysql_cur.execute("SELECT id FROM orders LIMIT 5000;")

                if len(items) >= BATCH_SIZE:
                    mysql_cur.executemany(
        order_ids = [row[0] for row in mysql_cur.fetchall()]
                        """
        if mysql_data:
                        INSERT INTO order_items
            mysql_cur.executemany(
                """
                INSERT INTO orders
                        (order_id, product_id, product_sku,
                (status, subtotal, tax, shipping_cost, total_amount, request_key, created_at)
                         product_name, product_category,
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                         quantity, unit_price, subtotal)
                """,
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                mysql_data,
            )
                        """,
            mysql_conn.commit()
                        items,

                    )
        print("Insertando order_items...")
                    mysql_conn.commit()
        print(f"✅ {remaining_orders} órdenes insertadas.")
    if items_count == 0:
                    items.clear()


        if items:
    items_count = mysql_cur.fetchone()[0]
            mysql_cur.executemany(
    else:
                """
                INSERT INTO order_items
    mysql_cur.execute("SELECT COUNT(*) FROM order_items;")
                (order_id, product_id, product_sku,
                 product_name, product_category,
    # ------------------------------------------------
                 quantity, unit_price, subtotal)

                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)

                """,

                items,

            )

            mysql_conn.commit()


        mysql_cur.execute("SELECT COUNT(*) FROM order_items;")
        total_items = mysql_cur.fetchone()[0]

        print(f"✅ {total_items} order_items disponibles.")
    else:
        print(f"✅ Ya existen {items_count} order_items.")

    mysql_cur.close()
    mysql_conn.close()


except Exception as e:
    print(f"❌ Error en MySQL: {e}")

# ====================================================
# 2. MONGODB (hardtech_inventory)
# ====================================================
print("\n=== 2. POBLANDO MONGODB (hardtech_inventory) ===")

try:
    mongo_client = MongoClient(
        "mongodb://inventory_app:inventory2026@localhost:27017/"
        "hardtech_inventory?authSource=hardtech_inventory"
    )

    mongo_db = mongo_client["hardtech_inventory"]

    # ------------------------------------------------
    # INVENTORY
    # ------------------------------------------------
    inventory = mongo_db["inventory"]

    inventory_count = inventory.count_documents({})

    if inventory_count < TOTAL_RECORDS:
        print(f"Insertando {TOTAL_RECORDS - inventory_count} inventarios...")

        docs = []

        for i in range(inventory_count + 1, TOTAL_RECORDS + 1):
            stock = random.randint(10, 500)
            reserved = random.randint(0, min(stock, 20))

            docs.append(

                {

                    "_id": i,

                    "stock": stock,

                    "reserved_stock": reserved,

                    "reorder_point": random.randint(5, 30),
                }

            )


            if len(docs) >= BATCH_SIZE:

                inventory.insert_many(docs)
                docs.clear()


        if docs:

            inventory.insert_many(docs)

        print("✅ Inventario poblado con 20,000 registros.")

    else:

        print(f"✅ Ya existen {inventory_count} registros de inventario.")


    # ------------------------------------------------
    # INVENTORY MOVEMENTS
    # ------------------------------------------------

    movements_collection = mongo_db["inventory_movements"]


    movement_count = movements_collection.count_documents({})


    if movement_count == 0:
        print("Insertando movimientos de inventario...")


        movement_types = [
            "STOCK_IN",
            "RESERVE",
            "RELEASE",

            "SALE",
            "ADJUSTMENT",
        ]

        movements = []

        for i in range(1, 2001):
            movements.append(
                {
                    "_id": i,
                    "product_id": random.randint(1, 100),
                    "movement_type": random.choice(movement_types),
                    "quantity": random.randint(1, 50),
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }
            )

            if len(movements) >= BATCH_SIZE:
                movements_collection.insert_many(movements)
                movements.clear()

        if movements:
            movements_collection.insert_many(movements)

        print("✅ 2,000 movimientos insertados.")
    else:
        print(f"✅ Ya existen {movement_count} movimientos.")

    mongo_client.close()

except Exception as e:
    print(f"❌ Error en MongoDB: {e}")

# ====================================================
print("\n🎉 CARGA COMPLETA Y VERIFICADA")
print("=" * 55)
