from datetime import datetime, timedelta
import timeit
import uuid
from faker import Faker
from google.cloud import datastore
from ..params import REPEAT, NUMBER, ACTIVITIES

fake = Faker()

PROJECT_ID = "YOUR_PROJECT_ID"
client = datastore.Client(PROJECT_ID)

id = 0
users = []
notifications: dict[str, list] = {}


def setup():
    global users, notifications
    # Resetting user and notifications lists
    users.clear()
    notifications.clear()

    # Optionally delete all entities if you want a clean slate each time.
    # Be very careful with this in production as this will erase data.
    query = client.query(kind="User")
    users_to_delete = list(query.fetch())
    for user in users_to_delete:
        client.delete(user.key)

    query = client.query(kind="Notification")
    notifications_to_delete = list(query.fetch())
    for notification in notifications_to_delete:
        client.delete(notification.key)


def insert():
    global id
    id += 1

    user_key = client.key("User", id)
    user = datastore.Entity(key=user_key)
    user.update(
        {
            "email": fake.email(),
            "username": fake.slug(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
        }
    )
    client.put(user)
    users.append(user.key.id)

    for _ in range(ACTIVITIES):
        expires_at = timedelta(days=1, hours=2, minutes=30)
        not_before = timedelta(days=0, hours=2, minutes=30)

        notification_key = client.key("Notification", uuid.uuid4().hex)
        notification = datastore.Entity(key=notification_key)
        notification.update(
            {
                "user_id": user.key.id,
                "kind": "PRODUCT",
                "not_before": datetime.utcnow() + not_before,
                "expires_at": datetime.utcnow() + expires_at,
                "subject": "Your product is ready",
                "message": "Your product is ready to be picked up",
                "status": "NEW",
            }
        )
        client.put(notification)

        if user.key.id not in notifications:
            notifications[user.key.id] = []
        notifications[user.key.id].append(notification.key.id)


def select():
    user_id = users.pop(0)
    user_key = client.key("User", user_id)
    user = client.get(user_key)

    for notification_id in notifications[user_id]:
        notification_key = client.key("Notification", notification_id)
        notification = client.get(notification_key)

    users.append(user_id)


def update():
    user_id = users.pop(0)
    user_key = client.key("User", user_id)
    user = client.get(user_key)
    user["email"] = fake.email()
    user["username"] = fake.slug()
    user["first_name"] = fake.first_name()
    user["last_name"] = fake.last_name()
    client.put(user)

    for notification_id in notifications[user_id]:
        notification_key = client.key("Notification", notification_id)
        notification = client.get(notification_key)
        notification["status"] = "SENT"
        client.put(notification)

    users.append(user_id)


def delete():
    user_id = users.pop(0)
    user_key = client.key("User", user_id)
    client.delete(user_key)

    for notification_id in notifications[user_id]:
        notification_key = client.key("Notification", notification_id)
        client.delete(notification_key)

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
