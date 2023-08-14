from datetime import datetime, timedelta
import timeit
import uuid
from faker import Faker
from google.cloud import firestore
from ..params import REPEAT, NUMBER, ACTIVITIES

fake = Faker()

PROJECT_ID = "YOUR_PROJECT_ID"
DB_COLLECTION = "notifications"

db = firestore.Client(project=PROJECT_ID)
collection_ref = db.collection(DB_COLLECTION)

id = 0
users = []
notifications: dict[str, list] = {}


def setup():
    global users, notifications
    users.clear()
    notifications.clear()


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
        ttl_seconds = int(expires_at.total_seconds())
        product_id = uuid.uuid4()

        notification_data = {
            "kind": "PRODUCT",
            "external_id": str(product_id),
            "not_before": datetime.utcnow() + not_before,
            "expires_at": datetime.utcnow() + expires_at,
            "subject": "Your product is ready",
            "message": "Your product is ready to be picked up",
            "status": "NEW",
            "user": user,
        }
        collection_ref.add(notification_data)

        if user["id"] not in notifications:
            notifications[user["id"]] = []

        notifications[user["id"]].append({"kind": "PRODUCT", "external_id": str(product_id)})


def select():
    user_id = users.pop(0)
    for kwargs in notifications[user_id]:
        notification_ref = (
            collection_ref.where("user.id", "==", user_id)
            .where("kind", "==", kwargs["kind"])
            .where("external_id", "==", kwargs["external_id"])
        )
        for doc in notification_ref.stream():
            pass  # do nothing as we're just selecting
    users.append(user_id)


def update():
    user_id = users.pop(0)
    for kwargs in notifications[user_id]:
        notification_ref = (
            collection_ref.where("user.id", "==", user_id)
            .where("kind", "==", kwargs["kind"])
            .where("external_id", "==", kwargs["external_id"])
        )
        for doc in notification_ref.stream():
            doc.reference.update(
                {
                    "status": "SENT",
                    "user.email": fake.email(),
                    "user.username": fake.slug(),
                    "user.first_name": fake.first_name(),
                    "user.last_name": fake.last_name(),
                }
            )
    users.append(user_id)


def delete():
    user_id = users.pop(0)
    for kwargs in notifications[user_id]:
        notification_ref = (
            collection_ref.where("user.id", "==", user_id)
            .where("kind", "==", kwargs["kind"])
            .where("external_id", "==", kwargs["external_id"])
        )
        for doc in notification_ref.stream():
            doc.reference.delete()
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
