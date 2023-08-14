from datetime import datetime, timedelta
import timeit
import uuid
import bson
from faker import Faker
from pymongo import MongoClient
from ..params import REPEAT, NUMBER, ACTIVITIES

fake = Faker()

users = []
notifications = {}

id = 0


def setup():
    global client, db, notification_collection, users, notifications

    client = MongoClient("localhost", 27017, username="root", password="example")
    # config = {
    #     "_id": "my-mongo-set",
    #     "members": [
    #         {"_id": 0, "host": "localhost:27011"},
    #         {"_id": 1, "host": "localhost:27012"},
    #         {"_id": 2, "host": "localhost:27013"},
    #     ],
    # }

    # client.admin.command("replSetInitiate", config)
    # client.admin.command("replSetInitiate")
    # client.admin.command("replSetAdd", "mongo2:27017")
    # client.admin.command("replSetAdd", "mongo3:27017")

    db = client["test"]
    notification_collection = db["notifications"]

    db.drop_collection("users")
    db.drop_collection("notifications")
    db.drop_collection("products")


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
        product_id = bson.Binary(product_id.bytes, 0x04)

        notification = {
            "kind": "PRODUCT",
            "external_id": product_id,
            "not_before": datetime.utcnow() + not_before,
            "expires_at": datetime.utcnow() + expires_at,
            "subject": "Your product is ready",
            "message": "Your product is ready to be picked up",
            "status": "NEW",
            "email": user["email"],
            "username": user["username"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
        }
        notification_collection.insert_one(notification)

        if user["id"] not in notifications:
            notifications[user["id"]] = []

        notifications[user["id"]].append(
            {
                "kind": "PRODUCT",
                "external_id": product_id,
            }
        )


def select():
    user_id = users.pop(0)
    for kwargs in notifications[user_id]:
        list(notification_collection.find(kwargs))

    users.append(user_id)


def update():
    user_id = users.pop(0)
    for kwargs in notifications[user_id]:
        notification_collection.update_many(
            kwargs,
            {
                "$set": {
                    "status": "SENT",
                    "email": fake.email(),
                    "username": fake.slug(),
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                }
            },
        )

    users.append(user_id)


def delete():
    user_id = users.pop(0)
    for kwargs in notifications[user_id]:
        notification_collection.delete_many(kwargs)

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
