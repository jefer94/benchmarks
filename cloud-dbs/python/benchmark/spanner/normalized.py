from datetime import datetime, timedelta
import timeit
from google.cloud import spanner
from faker import Faker
from ..params import REPEAT, NUMBER, ACTIVITIES

fake = Faker()

PROJECT_ID = "YOUR_PROJECT_ID"
INSTANCE_ID = "YOUR_INSTANCE_ID"
DATABASE_ID = "YOUR_DATABASE_ID"

spanner_client = spanner.Client(project=PROJECT_ID)
instance = spanner_client.instance(INSTANCE_ID)
database = instance.database(DATABASE_ID)

users = []
notifications: dict[str, list] = {}


def setup():
    global users, notifications
    users = []
    notifications = {}


def insert():
    user_columns = ["Email", "Username", "FirstName", "LastName"]
    user_values = [fake.email(), fake.slug(), fake.first_name(), fake.last_name()]

    with database.batch() as batch:
        batch.insert(table="User", columns=user_columns, values=[user_values])

    user_id = spanner_client.execute_sql(f"SELECT LAST_INSERT_ID()")[0][0]
    users.append(user_id)

    for _ in range(ACTIVITIES):
        product_columns = ["Name", "Amount"]
        product_values = ["John Doe", 100]

        with database.batch() as batch:
            batch.insert(table="Product", columns=product_columns, values=[product_values])

        sku = spanner_client.execute_sql(f"SELECT LAST_INSERT_ID()")[0][0]
        notification_columns = [
            "Kind",
            "ExternalId",
            "UserId",
            "NotBefore",
            "ExpiresAt",
            "Subject",
            "Message",
            "Status",
        ]
        notification_values = [
            "PRODUCT",
            sku,
            user_id,
            datetime.utcnow() + timedelta(hours=2, minutes=30),
            datetime.utcnow() + timedelta(days=1, hours=2, minutes=30),
            "Your product is ready",
            "Your product is ready to be picked up",
            "NEW",
        ]

        with database.batch() as batch:
            batch.insert(table="Notification", columns=notification_columns, values=[notification_values])

        notification_id = spanner_client.execute_sql(f"SELECT LAST_INSERT_ID()")[0][0]
        if user_id not in notifications:
            notifications[user_id] = []
        notifications[user_id].append(notification_id)


def select():
    user_id = users.pop(0)

    with database.snapshot() as snapshot:
        user = list(snapshot.execute_sql(f"SELECT * FROM User WHERE UserId = {user_id}"))
        for notification_id in notifications[user_id]:
            notification = list(
                snapshot.execute_sql(f"SELECT * FROM Notification WHERE NotificationId = {notification_id}")
            )

    users.append(user_id)


def update():
    user_id = users.pop(0)

    with database.batch() as batch:
        batch.update(
            table="User",
            columns=["UserId", "Email", "Username", "FirstName", "LastName"],
            values=[[user_id, fake.email(), fake.slug(), fake.first_name(), fake.last_name()]],
        )

        for notification_id in notifications[user_id]:
            batch.update(
                table="Notification", columns=["NotificationId", "Status"], values=[[notification_id, "SENT"]]
            )

    users.append(user_id)


def delete():
    user_id = users.pop(0)

    with database.batch() as batch:
        batch.delete(table="User", keys=[[user_id]])
        for notification_id in notifications[user_id]:
            batch.delete(table="Notification", keys=[[notification_id]])

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
