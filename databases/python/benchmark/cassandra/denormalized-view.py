from datetime import datetime, timedelta
import time
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
import timeit
import uuid
from faker import Faker
from cassandra.cqlengine.models import QuerySetDescriptor
from ..params import REPEAT, NUMBER, ACTIVITIES

fake = Faker()


class Notification(Model):
    __keyspace__ = "test"
    objects: QuerySetDescriptor

    kind = columns.Text(partition_key=True)
    external_id = columns.UUID(partition_key=True)

    not_before = columns.DateTime(primary_key=True)
    expires_at = columns.DateTime(primary_key=True)
    subject = columns.Text(primary_key=True)
    message = columns.Text(primary_key=True)

    status = columns.Text(static=True)

    # user related fields
    email = columns.Text()
    username = columns.Text()
    first_name = columns.Text()
    last_name = columns.Text()


class NotificationView(Model):
    __keyspace__ = "test"
    objects: QuerySetDescriptor

    kind = columns.Text(partition_key=True)
    external_id = columns.UUID(partition_key=True)

    not_before = columns.DateTime(primary_key=True)
    expires_at = columns.DateTime(primary_key=True)
    subject = columns.Text(primary_key=True)
    message = columns.Text(primary_key=True)

    # user related fields
    email = columns.Text()
    username = columns.Text()
    first_name = columns.Text()
    last_name = columns.Text()


cluster = None
users = []
notifications: dict[str, list] = {}


def setup():
    global cluster, notifications, users
    if not cluster:
        cluster = Cluster(contact_points=["localhost"], port=9042)

        session = cluster.connect()
        # session.set_keyspace("testkeyspace")
        connection.set_session(session)

        users = []
        notifications = {}
        session.execute(
            "CREATE KEYSPACE IF NOT EXISTS test WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }"
        )
        session.set_keyspace("test")
        session.execute("DROP MATERIALIZED VIEW IF EXISTS test.notification_view")
        session.execute("DROP TABLE IF EXISTS test.notification")

        sync_table(Notification)

        session.execute(
            """
            CREATE MATERIALIZED VIEW test.notification_view AS
                SELECT kind, external_id, not_before, expires_at, subject, message, email,
                    username, first_name, last_name
                FROM test.notification
                WHERE kind IS NOT NULL AND external_id IS NOT NULL AND not_before IS NOT NULL 
                    AND expires_at IS NOT NULL AND subject IS NOT NULL AND message IS NOT NULL
                PRIMARY KEY ((kind, external_id), not_before, expires_at, subject, message);
            """
        )


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
        # Create a timedelta object
        expires_at = timedelta(days=1, hours=2, minutes=30, seconds=0)
        not_before = timedelta(days=0, hours=2, minutes=30, seconds=0)

        # Convert timedelta to seconds
        ttl_seconds = int(expires_at.total_seconds())

        product_id = uuid.uuid4()

        Notification.create(
            kind="PRODUCT",
            external_id=product_id,
            not_before=datetime.utcnow() + not_before,
            expires_at=datetime.utcnow() + expires_at,
            subject="Your product is ready",
            message="Your product is ready to be picked up",
            status="NEW",
            email=user["email"],
            username=user["username"],
            first_name=user["first_name"],
            last_name=user["last_name"],
        ).ttl(ttl_seconds)

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
        for _ in NotificationView.objects(**kwargs):
            pass

    users.append(user_id)


def update():
    user_id = users.pop(0)
    for kwargs in notifications[user_id]:
        for x in Notification.objects(**kwargs):
            x.update(
                status="SENT",
                email=fake.email(),
                username=fake.slug(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
    users.append(user_id)


def delete():
    user_id = users.pop(0)
    for kwargs in notifications[user_id]:
        for x in Notification.objects(**kwargs):
            x.delete()

    users.append(user_id)


def main():
    total = 0
    time_took = timeit.repeat(insert, setup=setup, repeat=REPEAT, number=NUMBER)
    print(f"- Insert took {(sum(time_took) / len(time_took)):.6f} seconds")

    total += sum(time_took) / len(time_took)

    time.sleep(1)

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
