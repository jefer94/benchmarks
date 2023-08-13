from datetime import datetime, timedelta
import bson
from pymongo import MongoClient
import timeit
import uuid
from faker import Faker
from ..params import REPEAT, NUMBER, ACTIVITIES

fake = Faker()


users = []
notifications = {}


def setup():
    global notifications, users, users_collection, notifications_collection, products_collection

    client = MongoClient("localhost", 27011, username="root", password="example")
    # config = {
    #     "_id": "my-mongo-set",
    #     "members": [
    #         {"_id": 0, "host": "localhost:27011"},
    #         {"_id": 1, "host": "localhost:27012"},
    #         {"_id": 2, "host": "localhost:27013"},
    #     ],
    # }

    # client.admin.command("replSetInitiate", config)
    client.admin.command("replSetInitiate")
    client.admin.command("replSetAdd", "mongo2:27017")
    client.admin.command("replSetAdd", "mongo3:27017")

    db = client["test_db"]
    users_collection = db["users"]
    notifications_collection = db["notifications"]
    products_collection = db["products"]

    db.drop_collection("users")
    db.drop_collection("notifications")
    db.drop_collection("products")


def insert():
    global users

    user = {
        "email": fake.email(),
        "username": fake.slug(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
    }
    x = users_collection.insert_one(user)
    users.append(x.inserted_id)

    for _ in range(ACTIVITIES):
        product = {"name": "John Doe", "amount": 100}
        y = products_collection.insert_one(product)

        expires_at = timedelta(days=1, hours=2, minutes=30, seconds=0)
        not_before = timedelta(days=0, hours=2, minutes=30, seconds=0)
        ttl_seconds = int(expires_at.total_seconds())

        notification = {
            "kind": "PRODUCT",
            "external_id": product["_id"],
            "user_id": x.inserted_id,
            "not_before": datetime.utcnow() + not_before,
            "expires_at": datetime.utcnow() + expires_at,
            "subject": "Your product is ready",
            "message": "Your product is ready to be picked up",
            "status": "NEW",
            "ttl": ttl_seconds,
        }
        notifications_collection.insert_one(notification)

        if x.inserted_id not in notifications:
            notifications[x.inserted_id] = []

        notifications[x.inserted_id].append(
            {"kind": "PRODUCT", "external_id": y.inserted_id, "user_id": x.inserted_id}
        )


def select():
    global users

    user_id = users.pop(0)
    for _ in users_collection.find({"id": user_id}):
        pass

    for kwargs in notifications[user_id]:
        for _ in notifications_collection.find(kwargs):
            pass

    users.append(user_id)


def update():
    global users

    user_id = users.pop(0)
    user = {
        "email": fake.email(),
        "username": fake.slug(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
    }
    users_collection.update_one({"id": user_id}, {"$set": user})

    for kwargs in notifications[user_id]:
        notifications_collection.update_one(kwargs, {"$set": {"status": "SENT"}})

    users.append(user_id)


def delete():
    global users

    user_id = users.pop(0)
    users_collection.delete_one({"id": user_id})

    for kwargs in notifications[user_id]:
        notifications_collection.delete_one(kwargs)

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
