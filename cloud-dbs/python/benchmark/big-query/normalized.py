from datetime import datetime, timedelta
import timeit
from faker import Faker
from google.cloud import bigquery
from ..params import REPEAT, NUMBER, ACTIVITIES

fake = Faker()

PROJECT_ID = "YOUR_PROJECT_ID"
DATASET_ID = "YOUR_DATASET_ID"

bigquery_client = bigquery.Client(project=PROJECT_ID)
dataset_ref = bigquery_client.dataset(DATASET_ID)

users = []
notifications: dict[str, list] = {}


def setup():
    global users, notifications
    users = []
    notifications = {}


def insert():
    user_table_ref = dataset_ref.table("User")
    user_values = [(fake.email(), fake.slug(), fake.first_name(), fake.last_name())]

    user_errors = bigquery_client.insert_rows(user_table_ref, user_values)

    user_id_query = "SELECT MAX(UserId) as last_user_id FROM `User`"
    user_id = bigquery_client.query(user_id_query).result().to_dataframe().iloc[0]["last_user_id"]

    users.append(user_id)

    for _ in range(ACTIVITIES):
        product_table_ref = dataset_ref.table("Product")
        product_values = [("John Doe", 100)]

        product_errors = bigquery_client.insert_rows(product_table_ref, product_values)

        sku_query = "SELECT MAX(ProductId) as last_product_id FROM `Product`"
        sku = bigquery_client.query(sku_query).result().to_dataframe().iloc[0]["last_product_id"]

        notification_table_ref = dataset_ref.table("Notification")
        notification_values = [
            (
                "PRODUCT",
                sku,
                user_id,
                datetime.utcnow() + timedelta(hours=2, minutes=30),
                datetime.utcnow() + timedelta(days=1, hours=2, minutes=30),
                "Your product is ready",
                "Your product is ready to be picked up",
                "NEW",
            )
        ]
        notification_errors = bigquery_client.insert_rows(notification_table_ref, notification_values)

        notification_id_query = "SELECT MAX(NotificationId) as last_notification_id FROM `Notification`"
        notification_id = (
            bigquery_client.query(notification_id_query)
            .result()
            .to_dataframe()
            .iloc[0]["last_notification_id"]
        )
        if user_id not in notifications:
            notifications[user_id] = []
        notifications[user_id].append(notification_id)


def select():
    user_id = users.pop(0)

    user_query = f"SELECT * FROM `User` WHERE UserId = {user_id}"
    user = bigquery_client.query(user_query).result().to_dataframe()

    for notification_id in notifications[user_id]:
        notification_query = f"SELECT * FROM `Notification` WHERE NotificationId = {notification_id}"
        notification = bigquery_client.query(notification_query).result().to_dataframe()

    users.append(user_id)


def update():
    user_id = users.pop(0)

    user_update_query = f"""
    UPDATE `User`
    SET Email='{fake.email()}', Username='{fake.slug()}', FirstName='{fake.first_name()}', LastName='{fake.last_name()}'
    WHERE UserId = {user_id}
    """
    user_update_job = bigquery_client.query(user_update_query)
    user_update_job.result()

    for notification_id in notifications[user_id]:
        notification_update_query = f"""
        UPDATE `Notification`
        SET Status='SENT'
        WHERE NotificationId = {notification_id}
        """
        notification_update_job = bigquery_client.query(notification_update_query)
        notification_update_job.result()

    users.append(user_id)


def delete():
    user_id = users.pop(0)

    user_delete_query = f"DELETE FROM `User` WHERE UserId = {user_id}"
    user_delete_job = bigquery_client.query(user_delete_query)
    user_delete_job.result()

    for notification_id in notifications[user_id]:
        notification_delete_query = f"DELETE FROM `Notification` WHERE NotificationId = {notification_id}"
        notification_delete_job = bigquery_client.query(notification_delete_query)
        notification_delete_job.result()

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
