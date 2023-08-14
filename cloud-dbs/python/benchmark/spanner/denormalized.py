from datetime import datetime, timedelta
import timeit
import uuid
from faker import Faker
from google.cloud import spanner
from ..params import REPEAT, NUMBER, ACTIVITIES

fake = Faker()

PROJECT_ID = "YOUR_PROJECT_ID"
INSTANCE_ID = "YOUR_INSTANCE_ID"
DATABASE_ID = "YOUR_DATABASE_ID"

spanner_client = spanner.Client(project=PROJECT_ID)
instance = spanner_client.instance(INSTANCE_ID)
database = instance.database(DATABASE_ID)

id = 0
users = []
notifications: dict[str, list] = {}


def setup():
    global users, notifications
    # Resetting user and notifications lists
    users.clear()
    notifications.clear()

    # Deleting previous records (Use with caution!)
    with database.batch() as batch:
        batch.delete("User", keys=[[user_id] for user_id in users])
        for user_id in notifications.keys():
            batch.delete(
                "Notification",
                keys=[[user_id, notification_id] for notification_id in notifications[user_id]],
            )


def insert():
    global id
    id += 1

    user = {
        "UserId": id,
        "Email": fake.email(),
        "Username": fake.slug(),
        "FirstName": fake.first_name(),
        "LastName": fake.last_name(),
    }
    with database.batch() as batch:
        batch.insert(table="User", columns=user.keys(), values=[user.values()])

    users.append(id)

    notifications[id] = []
    for _ in range(ACTIVITIES):
        expires_at = datetime.utcnow() + timedelta(days=1, hours=2, minutes=30)
        not_before = datetime.utcnow() + timedelta(days=0, hours=2, minutes=30)
        notification_id = uuid.uuid4().hex

        notification = {
            "UserId": id,
            "NotificationId": notification_id,
            "Kind": "PRODUCT",
            "NotBefore": not_before,
            "ExpiresAt": expires_at,
            "Subject": "Your product is ready",
            "Message": "Your product is ready to be picked up",
            "Status": "NEW",
        }

        with database.batch() as batch:
            batch.insert(table="Notification", columns=notification.keys(), values=[notification.values()])

        notifications[id].append(notification_id)


def select():
    user_id = users.pop(0)

    with database.snapshot() as snapshot:
        user = list(snapshot.execute_sql(f"SELECT * FROM User WHERE UserId = {user_id}"))
        for notification_id in notifications[user_id]:
            notification = list(
                snapshot.execute_sql(
                    f"SELECT * FROM Notification WHERE UserId = {user_id} AND NotificationId = '{notification_id}'"
                )
            )

    users.append(user_id)


def update():
    user_id = users.pop(0)
    new_user_data = {
        "Email": fake.email(),
        "Username": fake.slug(),
        "FirstName": fake.first_name(),
        "LastName": fake.last_name(),
    }

    with database.batch() as batch:
        batch.update(
            table="User", columns=new_user_data.keys(), values=[[user_id] + list(new_user_data.values())]
        )

        for notification_id in notifications[user_id]:
            batch.update(
                table="Notification",
                columns=["UserId", "NotificationId", "Status"],
                values=[[user_id, notification_id, "SENT"]],
            )

    users.append(user_id)


def delete():
    user_id = users.pop(0)

    with database.batch() as batch:
        batch.delete("User", keys=[[user_id]])
        for notification_id in notifications[user_id]:
            batch.delete("Notification", keys=[[user_id, notification_id]])

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
