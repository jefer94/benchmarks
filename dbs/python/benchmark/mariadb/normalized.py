from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
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


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(60))
    username = Column(String(30))
    first_name = Column(String(60))
    last_name = Column(String(60))


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    amount = Column(Integer)


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    kind = Column(String(20))
    external_id = Column(String(60))
    user_id = Column(Integer, ForeignKey("users.id"))
    not_before = Column(DateTime)
    expires_at = Column(DateTime)
    subject = Column(String(60))
    message = Column(String(60))
    status = Column(String(20))


drop = True
users = []
notifications = {}


def setup():
    global users, notifications, session, drop

    if drop:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        drop = False


def insert():
    user = User(
        email=fake.email(),
        username=fake.slug(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )
    session.add(user)
    session.commit()

    users.append(user.id)

    for _ in range(ACTIVITIES):
        product = Product(name="John Doe", amount=100)
        session.add(product)
        session.commit()

        expires_at = datetime.utcnow() + timedelta(days=1, hours=2, minutes=30)
        not_before = datetime.utcnow() + timedelta(hours=2, minutes=30)

        notification = Notification(
            kind="PRODUCT",
            external_id=product.id,
            user_id=user.id,
            not_before=not_before,
            expires_at=expires_at,
            subject="Your product is ready",
            message="Your product is ready to be picked up",
            status="NEW",
        )
        session.add(notification)
        session.commit()

        if user.id not in notifications:
            notifications[user.id] = []
        notifications[user.id].append(notification.id)


def select():
    user_id = users.pop(0)
    user = session.query(User).filter_by(id=user_id).first()

    for notification_id in notifications[user_id]:
        for _ in session.query(Notification).filter_by(id=notification_id):
            pass

    users.append(user_id)


def update():
    user_id = users.pop(0)
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.email = fake.email()
        user.username = fake.slug()
        user.first_name = fake.first_name()
        user.last_name = fake.last_name()
        session.commit()

    for notification_id in notifications[user_id]:
        notification = session.query(Notification).filter_by(id=notification_id).first()
        if notification:
            notification.status = "SENT"
            session.commit()

    users.append(user_id)


def delete():
    user_id = users.pop(0)

    for notification_id in notifications[user_id]:
        notification = session.query(Notification).filter_by(id=notification_id).first()
        if notification:
            session.delete(notification)
            session.commit()

    user = session.query(User).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()


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
