from datetime import datetime, timedelta
import timeit
import uuid
import happybase
from faker import Faker
from ..params import REPEAT, NUMBER, ACTIVITIES

fake = Faker()

connection = None
table = None
users = []
notifications = {}


def setup():
    global connection, table, notifications, users

    connection = happybase.Connection("localhost")
    table_name = "notifications"

    # If table exists, drop it and recreate
    if table_name.encode() in connection.tables():
        connection.delete_table(table_name, disable=True)

    # Create a table with column family 'cf'
    connection.create_table(table_name, {"cf": {}})
    table = connection.table(table_name)


id = 0


def insert():
    global id
    id += 1

    user = {
        "id": id,
        "email": fake.email(),
        "username": fake.slug(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
    }

    users.append(user["id"])

    for _ in range(ACTIVITIES):
        expires_at = timedelta(days=1, hours=2, minutes=30, seconds=0)
        not_before = timedelta(days=0, hours=2, minutes=30, seconds=0)

        product_id = uuid.uuid4()

        row_key = f"PRODUCT_{product_id}"
        table.put(
            row_key,
            {
                "cf:not_before": (datetime.utcnow() + not_before).strftime("%Y-%m-%d %H:%M:%S"),
                "cf:expires_at": (datetime.utcnow() + expires_at).strftime("%Y-%m-%d %H:%M:%S"),
                "cf:subject": "Your product is ready",
                "cf:message": "Your product is ready to be picked up",
                "cf:status": "NEW",
                "cf:email": user["email"],
                "cf:username": user["username"],
                "cf:first_name": user["first_name"],
                "cf:last_name": user["last_name"],
            },
        )

        if user["id"] not in notifications:
            notifications[user["id"]] = []

        notifications[user["id"]].append(
            {
                "row_key": row_key,
            }
        )


def select():
    user_id = users.pop(0)
    for kwargs in notifications[user_id]:
        data = table.row(kwargs["row_key"])
        # Process data if needed
    users.append(user_id)


def update():
    user_id = users.pop(0)
    for kwargs in notifications[user_id]:
        table.put(
            kwargs["row_key"],
            {
                "cf:status": "SENT",
                "cf:email": fake.email(),
                "cf:username": fake.slug(),
                "cf:first_name": fake.first_name(),
                "cf:last_name": fake.last_name(),
            },
        )
    users.append(user_id)


def delete():
    user_id = users.pop(0)
    for kwargs in notifications[user_id]:
        table.delete(kwargs["row_key"])
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
