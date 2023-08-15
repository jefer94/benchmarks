from datetime import datetime, timedelta
import uuid
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, UUID
from sqlalchemy.orm import sessionmaker, declarative_base
import timeit
from faker import Faker
from ..params import REPEAT, NUMBER, ACTIVITIES

Base = declarative_base()
fake = Faker()

engine = create_engine(
    "mysql+pymysql://postgres:example@localhost:3307/postgres",
    pool_size=1000,
    max_overflow=2000,
    connect_args={"connect_timeout": 10},
)
Session = sessionmaker(bind=engine)
session = Session()


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    kind = Column(String(20))
    external_id = Column(UUID)
    not_before = Column(DateTime)
    expires_at = Column(DateTime)
    subject = Column(String(60))
    message = Column(String(60))
    status = Column(String(20))
    email = Column(String(60))
    username = Column(String(30))
    first_name = Column(String(60))
    last_name = Column(String(60))


drop = True
users = []
notifications = {}


def setup():
    global users, notifications, session, drop

    if drop:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        drop = False


users = []
notifications: dict[int, list] = {}


def insert():
    session = Session()
    user_id = len(users) + 1
    user = {
        "id": user_id,
        "email": fake.email(),
        "username": fake.slug(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
    }
    users.append(user_id)

    for _ in range(ACTIVITIES):
        expires_at = timedelta(days=1, hours=2, minutes=30, seconds=0)
        not_before = timedelta(days=0, hours=2, minutes=30, seconds=0)
        product_id = uuid.uuid4()
        notification = Notification(
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
        )
        session.add(notification)

        if user["id"] not in notifications:
            notifications[user["id"]] = []

        notifications[user["id"]].append(
            {
                "kind": "PRODUCT",
                "external_id": product_id,
            }
        )

    session.commit()


def select():
    user_id = users.pop(0)
    session = Session()
    for kwargs in notifications[user_id]:
        notification = session.query(Notification).filter(
            Notification.kind == kwargs["kind"], Notification.external_id == kwargs["external_id"]
        )
        for _ in notification.all():
            pass
    users.append(user_id)


def update():
    user_id = users.pop(0)
    session = Session()

    for kwargs in notifications[user_id]:
        l = session.query(Notification).filter(
            Notification.kind == kwargs["kind"], Notification.external_id == kwargs["external_id"]
        )
        for notification in l:
            notification.status = "SENT"
            notification.email = fake.email()
            notification.username = fake.slug()
            notification.first_name = fake.first_name()
            notification.last_name = fake.last_name()

    users.append(user_id)
    session.commit()


def delete():
    user_id = users.pop(0)
    session = Session()
    for kwargs in notifications[user_id]:
        l = session.query(Notification).filter(
            Notification.kind == kwargs["kind"], Notification.external_id == kwargs["external_id"]
        )
        for notification in l:
            session.delete(notification)
    session.commit()


# ... Remaining code (like the main function) stays the same.
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
