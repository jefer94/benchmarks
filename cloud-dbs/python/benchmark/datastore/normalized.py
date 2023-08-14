from datetime import datetime, timedelta
import timeit
from google.cloud import datastore
from faker import Faker
from ..params import REPEAT, NUMBER, ACTIVITIES

fake = Faker()

client = datastore.Client()
kind_user = "User"
kind_notification = "Notification"
kind_product = "Product"

users = []
notifications: dict[str, list] = {}


def setup():
    global users, notifications
    users = []
    notifications = {}

    # In Datastore, deleting entire kinds isn't straightforward. For simplicity, we'll just reset our lists.
    # If you need to delete entities, you'll need to query for them and delete them individually.


def insert():
    user_key = client.key(kind_user)
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
    user_id = user.key.id
    users.append(user_id)

    for _ in range(ACTIVITIES):
        product_key = client.key(kind_product)
        product = datastore.Entity(key=product_key)
        product["name"] = "John Doe"
        product["amount"] = 100
        client.put(product)

        sku = product.key.id
        notification_key = client.key(kind_notification)
        notification = datastore.Entity(key=notification_key)
        notification.update(
            {
                "kind": "PRODUCT",
                "external_id": sku,
                "user_id": user_id,
                "not_before": datetime.utcnow() + timedelta(hours=2, minutes=30),
                "expires_at": datetime.utcnow() + timedelta(days=1, hours=2, minutes=30),
                "subject": "Your product is ready",
                "message": "Your product is ready to be picked up",
                "status": "NEW",
            }
        )
        client.put(notification)

        if user_id not in notifications:
            notifications[user_id] = []
        notifications[user_id].append(notification.key.id)


def select():
    user_id = users.pop(0)
    user_key = client.key(kind_user, user_id)
    user = client.get(user_key)

    for notification_id in notifications[user_id]:
        notification_key = client.key(kind_notification, notification_id)
        notification = client.get(notification_key)

    users.append(user_id)


def update():
    user_id = users.pop(0)
    user_key = client.key(kind_user, user_id)
    user = client.get(user_key)

    if user:
        user["email"] = fake.email()
        user["username"] = fake.slug()
        user["first_name"] = fake.first_name()
        user["last_name"] = fake.last_name()
        client.put(user)

        for notification_id in notifications[user_id]:
            notification_key = client.key(kind_notification, notification_id)
            notification = client.get(notification_key)
            notification["status"] = "SENT"
            client.put(notification)

    users.append(user_id)


def delete():
    user_id = users.pop(0)
    user_key = client.key(kind_user, user_id)
    client.delete(user_key)

    for notification_id in notifications[user_id]:
        notification_key = client.key(kind_notification, notification_id)
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
