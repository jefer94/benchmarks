from datetime import datetime, timedelta
import timeit
from faker import Faker
from google.cloud import firestore
from ..params import REPEAT, NUMBER, ACTIVITIES

fake = Faker()

db = firestore.Client()

users = []
notifications: dict[str, list] = {}


def setup():
    global users, notifications
    users = []
    notifications = {}

    # Cleanup collections (this is naive; use with caution)
    for doc in db.collection("user").stream():
        doc.reference.delete()

    for doc in db.collection("notification").stream():
        doc.reference.delete()

    for doc in db.collection("product").stream():
        doc.reference.delete()


def insert():
    user_id = str(fake.uuid4())
    email = fake.email()
    username = fake.slug()
    first_name = fake.first_name()
    last_name = fake.last_name()

    db.collection("user").document(user_id).set(
        {"email": email, "username": username, "first_name": first_name, "last_name": last_name}
    )

    users.append(user_id)

    for _ in range(ACTIVITIES):
        sku = str(fake.uuid4())
        db.collection("product").document(sku).set({"name": "John Doe", "amount": "100"})

        not_before = (datetime.utcnow() + timedelta(hours=2, minutes=30)).isoformat()
        expires_at = (datetime.utcnow() + timedelta(days=1, hours=2, minutes=30)).isoformat()

        db.collection("notification").add(
            {
                "kind": "PRODUCT",
                "not_before": not_before,
                "expires_at": expires_at,
                "subject": "Your product is ready",
                "message": "Your product is ready to be picked up",
                "status": "NEW",
                "user_id": user_id,
                "sku": sku,
            }
        )

        if user_id not in notifications:
            notifications[user_id] = []
        notifications[user_id].append(sku)


def select():
    user_id = users.pop(0)

    # Retrieving user data
    user_ref = db.collection("user").document(user_id)
    user = user_ref.get()
    if user.exists:
        pass  # Do something with the user data

    for sku in notifications[user_id]:
        notifications_ref = (
            db.collection("notification").where("user_id", "==", user_id).where("sku", "==", sku).stream()
        )
        for notification in notifications_ref:
            pass  # Do something with the notification data

    users.append(user_id)


def update():
    user_id = users.pop(0)

    user_ref = db.collection("user").document(user_id)
    user = user_ref.get()

    if user.exists:
        user_ref.update(
            {
                "email": fake.email(),
                "username": fake.slug(),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
            }
        )

        for sku in notifications[user_id]:
            notifications_ref = (
                db.collection("notification").where("user_id", "==", user_id).where("sku", "==", sku).stream()
            )
            for notification in notifications_ref:
                notification.reference.update({"status": "SENT"})

    users.append(user_id)


def delete():
    user_id = users.pop(0)

    user_ref = db.collection("user").document(user_id)
    user_ref.delete()

    for sku in notifications[user_id]:
        notifications_ref = (
            db.collection("notification").where("user_id", "==", user_id).where("sku", "==", sku).stream()
        )
        for notification in notifications_ref:
            notification.reference.delete()

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
