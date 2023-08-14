from datetime import datetime, timedelta
import timeit
import uuid
from faker import Faker
from google.cloud import bigquery
from ..params import REPEAT, NUMBER, ACTIVITIES

fake = Faker()

PROJECT_ID = "YOUR_PROJECT_ID"
DATASET_ID = "YOUR_DATASET_ID"
TABLE_USER = "User"
TABLE_NOTIFICATION = "Notification"

bq_client = bigquery.Client(project=PROJECT_ID)
dataset_ref = bq_client.dataset(DATASET_ID)

id = 0
users = []
notifications: dict[str, list] = {}


def setup():
    global users, notifications
    users.clear()
    notifications.clear()

    # Deleting previous records in BigQuery is costly (involves rewriting tables)
    # For benchmarking purpose, consider creating new tables or datasets instead of deleting records.


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

    # Inserting user
    user_table_ref = dataset_ref.table(TABLE_USER)
    user_insert_job = bq_client.insert_rows_json(user_table_ref, [user])
    user_insert_job.result()

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

        # Inserting notification
        notification_table_ref = dataset_ref.table(TABLE_NOTIFICATION)
        notification_insert_job = bq_client.insert_rows_json(notification_table_ref, [notification])
        notification_insert_job.result()

        notifications[id].append(notification_id)


def select():
    user_id = users.pop(0)

    # Selecting user
    user_sql = f"SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_USER}` WHERE UserId = {user_id}"
    user_query_job = bq_client.query(user_sql)
    user_result = user_query_job.result()

    # Selecting notifications
    for notification_id in notifications[user_id]:
        notification_sql = f"SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_NOTIFICATION}` WHERE UserId = {user_id} AND NotificationId = '{notification_id}'"
        notification_query_job = bq_client.query(notification_sql)
        notification_result = notification_query_job.result()

    users.append(user_id)


def update():
    # BigQuery doesn't support transactional updates; You might have to perform operations in a more roundabout manner
    # For benchmarking, consider just doing a select or avoid updates on BigQuery

    pass


def delete():
    # BigQuery doesn't support direct deletes like traditional databases.
    # You might have to recreate tables or datasets, or avoid deletions for benchmarking.

    pass


def main():
    total = 0

    # Measure insert
    time_took = timeit.repeat(insert, setup=setup, repeat=REPEAT, number=NUMBER)
    print(f"Insert took {(sum(time_took) / len(time_took)):.6f} seconds")
    total += sum(time_took) / len(time_took)

    # Measure select
    time_took = timeit.repeat(select, setup=setup, repeat=REPEAT, number=NUMBER)
    print(f"Select took {(sum(time_took) / len(time_took)):.6f} seconds")
    total += sum(time_took) / len(time_took)

    # For Update and Delete: Since BigQuery doesn't handle these operations in traditional manners, you might skip them or handle them differently.

    print(f"Total took {total:.6f} seconds")


if __name__ == "__main__":
    main()
