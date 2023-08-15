import datetime
import uuid
import timeit
from faker import Faker
import happybase
from ..params import REPEAT, NUMBER, ACTIVITIES

fake = Faker()

# HBase connection
connection = happybase.Connection(host="localhost", port=9090)
connection.open()

users = []
notifications: dict[str, list] = {}


def setup():
    global connection, users, notifications

    for name in ["user", "notification", "product"]:
        try:
            connection.delete_table(name, disable=True)
        except:
            pass
        connection.create_table(name, {"data": dict()})


def insert():
    user_table = connection.table("user")
    notification_table = connection.table("notification")
    product_table = connection.table("product")

    user_id = str(uuid.uuid4())
    user_data = {
        "data:email": fake.email(),
        "data:username": fake.slug(),
        "data:first_name": fake.first_name(),
        "data:last_name": fake.last_name(),
    }
    user_table.put(user_id, user_data)

    users.append(user_id)

    for _ in range(ACTIVITIES):
        product_id = str(uuid.uuid4())
        product_data = {"data:name": "John Doe", "data:amount": str(100)}
        product_table.put(product_id, product_data)

        notification_data = {
            "data:kind": "PRODUCT",
            "data:external_id": product_id,
            "data:user_id": user_id,
            "data:not_before": str(datetime.datetime.utcnow()),
            "data:expires_at": str(
                datetime.datetime.utcnow() + datetime.timedelta(days=1, hours=2, minutes=30)
            ),
            "data:subject": "Your product is ready",
            "data:message": "Your product is ready to be picked up",
            "data:status": "NEW",
        }
        notification_id = f"{user_id}_{product_id}"
        notification_table.put(notification_id, notification_data)

        if user_id not in notifications:
            notifications[user_id] = []
        notifications[user_id].append(notification_id)


def select():
    user_id = users.pop(0)
    user_table = connection.table("user")
    user = user_table.row(user_id)

    notification_table = connection.table("notification")
    for notification_id in notifications[user_id]:
        notification = notification_table.row(notification_id)

    users.append(user_id)


def update():
    user_id = users.pop(0)
    user_table = connection.table("user")
    user_data = {
        "data:email": fake.email(),
        "data:username": fake.slug(),
        "data:first_name": fake.first_name(),
        "data:last_name": fake.last_name(),
    }
    user_table.put(user_id, user_data)

    notification_table = connection.table("notification")
    for notification_id in notifications[user_id]:
        notification_data = {"data:status": "SENT"}
        notification_table.put(notification_id, notification_data)
    users.append(user_id)


def delete():
    user_id = users.pop(0)
    user_table = connection.table("user")
    user_table.delete(user_id)

    notification_table = connection.table("notification")
    for notification_id in notifications[user_id]:
        notification_table.delete(notification_id)

    users.append(user_id)


def main():
    total = 0
    time_took = timeit.repeat(insert, setup=setup, repeat=REPEAT, number=NUMBER)
    print(f"- Insert took {(sum(time_took) / len(time_took)):.6f} seconds")
    total += sum(time_took) / len(time_took)

    time_took = timeit.repeat(select, setup=setup, repeat=REPEAT, number=NUMBER)
    print(f"- Select took {(sum(time_took) / len(time_took)):.6f} seconds")
    total += sum(time_took) / len(time_took)

    time_took = timeit.repeat(update, setup=setup, repeat=REPEAT, number=NUMBER)
    print(f"- Update took {(sum(time_took) / len(time_took)):.6f} seconds")
    total += sum(time_took) / len(time_took)

    time_took = timeit.repeat(delete, setup=setup, repeat=REPEAT, number=NUMBER)
    print(f"- Delete took {(sum(time_took) / len(time_took)):.6f} seconds")
    total += sum(time_took) / len(time_took)

    print(f"- Total took {total:.6f} seconds")


if __name__ == "__main__":
    main()
