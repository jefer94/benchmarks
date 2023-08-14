from datetime import datetime, timedelta
import timeit
from google.cloud import bigtable
from google.cloud.bigtable import column_family, row_filters
from faker import Faker
from ..params import REPEAT, NUMBER, ACTIVITIES

fake = Faker()

client = bigtable.Client(admin=True)
instance = client.instance("YOUR_INSTANCE_NAME")  # Replace with your instance name
column_family_id = "cf1"

users = []
notifications: dict[str, list] = {}


def setup():
    global users, notifications
    users = []
    notifications = {}

    table_ids = [table.name.split("/")[-1] for table in instance.list_tables()]

    if "user" in table_ids:
        table = instance.table("user")
        table.delete()
    table = instance.table("user")
    cf = table.column_family(column_family_id)
    cf.create()

    if "notification" in table_ids:
        table = instance.table("notification")
        table.delete()
    table = instance.table("notification")
    cf = table.column_family(column_family_id)
    cf.create()

    if "product" in table_ids:
        table = instance.table("product")
        table.delete()
    table = instance.table("product")
    cf = table.column_family(column_family_id)
    cf.create()


def insert():
    user_table = instance.table("user")
    notification_table = instance.table("notification")
    product_table = instance.table("product")

    user_id = str(fake.uuid4())
    email = fake.email()
    username = fake.slug()
    first_name = fake.first_name()
    last_name = fake.last_name()

    user_row = user_table.row(user_id)
    user_row.set_cell(column_family_id, "email", email)
    user_row.set_cell(column_family_id, "username", username)
    user_row.set_cell(column_family_id, "first_name", first_name)
    user_row.set_cell(column_family_id, "last_name", last_name)
    user_table.mutate_rows([user_row])

    users.append(user_id)

    for _ in range(ACTIVITIES):
        sku = str(fake.uuid4())
        product_row = product_table.row(sku)
        product_row.set_cell(column_family_id, "name", "John Doe")
        product_row.set_cell(column_family_id, "amount", "100")
        product_table.mutate_rows([product_row])

        not_before = (datetime.utcnow() + timedelta(hours=2, minutes=30)).isoformat()
        expires_at = (datetime.utcnow() + timedelta(days=1, hours=2, minutes=30)).isoformat()

        notification_row = notification_table.row(f"{user_id}_{sku}")
        notification_row.set_cell(column_family_id, "kind", "PRODUCT")
        notification_row.set_cell(column_family_id, "not_before", not_before)
        notification_row.set_cell(column_family_id, "expires_at", expires_at)
        notification_row.set_cell(column_family_id, "subject", "Your product is ready")
        notification_row.set_cell(column_family_id, "message", "Your product is ready to be picked up")
        notification_row.set_cell(column_family_id, "status", "NEW")
        notification_table.mutate_rows([notification_row])

        if user_id not in notifications:
            notifications[user_id] = []
        notifications[user_id].append(sku)


def select():
    user_id = users.pop(0)
    user_table = instance.table("user")
    user = user_table.read_row(user_id)
    if user:
        pass  # Do something with the user data

    for sku in notifications[user_id]:
        notification_table = instance.table("notification")
        row_key = f"{user_id}_{sku}"
        notification = notification_table.read_row(row_key)
        if notification:
            pass  # Do something with the notification data

    users.append(user_id)


def update():
    user_id = users.pop(0)
    user_table = instance.table("user")
    user = user_table.read_row(user_id)
    if user:
        # Updating user
        user.set_cell(column_family_id, "email", fake.email())
        user.set_cell(column_family_id, "username", fake.slug())
        user.set_cell(column_family_id, "first_name", fake.first_name())
        user.set_cell(column_family_id, "last_name", fake.last_name())
        user_table.mutate_rows([user])

        # Updating associated notifications
        for sku in notifications[user_id]:
            notification_table = instance.table("notification")
            row_key = f"{user_id}_{sku}"
            notification = notification_table.read_row(row_key)
            if notification:
                notification.set_cell(column_family_id, "status", "SENT")
                notification_table.mutate_rows([notification])

    users.append(user_id)


def delete():
    user_id = users.pop(0)
    user_table = instance.table("user")
    user = user_table.read_row(user_id)
    if user:
        user.delete()
        user_table.mutate_rows([user])

        # Deleting associated notifications
        for sku in notifications[user_id]:
            notification_table = instance.table("notification")
            row_key = f"{user_id}_{sku}"
            notification = notification_table.read_row(row_key)
            if notification:
                notification.delete()
                notification_table.mutate_rows([notification])

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
