from datetime import datetime, timedelta
import timeit
import uuid
from faker import Faker
from google.cloud import bigtable
from google.cloud.bigtable import column_family, row_filters
from ..params import REPEAT, NUMBER, ACTIVITIES

fake = Faker()

PROJECT_ID = "YOUR_PROJECT_ID"
INSTANCE_ID = "YOUR_INSTANCE_ID"
TABLE_ID = "notifications"

client = bigtable.Client(project=PROJECT_ID, admin=True)
instance = client.instance(INSTANCE_ID)
table = instance.table(TABLE_ID)

id = 0
users = []
notifications: dict[str, list] = {}


def setup():
    global table
    if not table.exists():
        table.create()
        cf1 = table.column_family("cf1")
        cf1.create()
    users.clear()
    notifications.clear()


def insert():
    global id, table
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
        ttl_seconds = int(expires_at.total_seconds())
        product_id = uuid.uuid4()

        row_key = f"notification#{id}"
        row = table.direct_row(row_key)
        row.set_cell("cf1", "kind", "PRODUCT")
        row.set_cell("cf1", "external_id", str(product_id))
        row.set_cell("cf1", "not_before", str(datetime.utcnow() + not_before))
        row.set_cell("cf1", "expires_at", str(datetime.utcnow() + expires_at))
        row.set_cell("cf1", "subject", "Your product is ready")
        row.set_cell("cf1", "message", "Your product is ready to be picked up")
        row.set_cell("cf1", "status", "NEW")
        row.set_cell("cf1", "email", user["email"])
        row.set_cell("cf1", "username", user["username"])
        row.set_cell("cf1", "first_name", user["first_name"])
        row.set_cell("cf1", "last_name", user["last_name"])
        row.commit()

        if user["id"] not in notifications:
            notifications[user["id"]] = []

        notifications[user["id"]].append({"kind": "PRODUCT", "external_id": str(product_id)})


def select():
    global table
    user_id = users.pop(0)
    for kwargs in notifications[user_id]:
        row_key = f"notification#{user_id}"
        row = table.read_row(row_key)
    users.append(user_id)


def update():
    global table
    user_id = users.pop(0)
    for kwargs in notifications[user_id]:
        row_key = f"notification#{user_id}"
        row = table.direct_row(row_key)
        row.set_cell("cf1", "status", "SENT")
        row.set_cell("cf1", "email", fake.email())
        row.set_cell("cf1", "username", fake.slug())
        row.set_cell("cf1", "first_name", fake.first_name())
        row.set_cell("cf1", "last_name", fake.last_name())
        row.commit()
    users.append(user_id)


def delete():
    global table
    user_id = users.pop(0)
    for kwargs in notifications[user_id]:
        row_key = f"notification#{user_id}"
        row = table.direct_row(row_key)
        row.delete()
        row.commit()
    users.append(user_id)


def main():
    total = 0
    time_took = timeit.repeat(insert, setup=setup, repeat=REPEAT, number=NUMBER)
    print(f"Insert took {(sum(time_took) / len(time_took)):.6f} seconds")

    total += sum(time_took) / len(time_took)

    time_took = timeit.repeat(select, setup=setup, repeat=REPEAT, number=NUMBER)
    print(f"Select took {(sum(time_took) / len(time_took)):.6f} seconds")

    total += sum(time_took) / len(time_took)

    time_took = timeit.repeat(update, setup=setup, repeat=REPEAT, number=NUMBER)
    print(f"Update took {(sum(time_took) / len(time_took)):.6f} seconds")

    total += sum(time_took) / len(time_took)

    time_took = timeit.repeat(delete, setup=setup, repeat=REPEAT, number=NUMBER)
    print(f"Delete took {(sum(time_took) / len(time_took)):.6f} seconds")

    total += sum(time_took) / len(time_took)

    print(f"Total took {total:.6f} seconds")


if __name__ == "__main__":
    main()
