from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import timeit
from faker import Faker
from ..params import REPEAT, NUMBER, ACTIVITIES

Base = declarative_base()
fake = Faker()

engine = create_engine("postgresql://postgres:example@localhost:5432/postgres", pool_size=40, max_overflow=80)
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    kind = Column(String)
    external_id = Column(Integer)
    not_before = Column(DateTime)
    expires_at = Column(DateTime)
    subject = Column(String)
    message = Column(String)
    status = Column(String)


def setup():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


users = []
notifications: dict[int, list] = {}


def insert():
    session = Session()

    user = User(
        email=fake.email(), username=fake.slug(), first_name=fake.first_name(), last_name=fake.last_name()
    )
    session.add(user)
    session.flush()

    users.append(user.id)

    for _ in range(ACTIVITIES):
        expires_at = datetime.utcnow() + timedelta(days=1, hours=2, minutes=30, seconds=0)
        not_before = datetime.utcnow() + timedelta(days=0, hours=2, minutes=30, seconds=0)

        product_id = len(notifications) + 1  # rudimentary unique ID generation

        notification = Notification(
            kind="PRODUCT",
            external_id=product_id,
            user_id=user.id,
            not_before=not_before,
            expires_at=expires_at,
            subject="Your product is ready",
            message="Your product is ready to be picked up",
            status="NEW",
        )

        session.add(notification)

        if user.id not in notifications:
            notifications[user.id] = []
        notifications[user.id].append({"kind": "PRODUCT", "external_id": product_id})

    session.commit()


def select():
    session = Session()
    user_id = users[0]  # Get the first user without removing from the list

    for notif in session.query(Notification).filter_by(user_id=user_id):
        pass  # Process the notification if needed


def update():
    session = Session()

    user_id = users[0]  # Get the first user without removing from the list

    for notif in session.query(Notification).filter_by(user_id=user_id):
        notif.status = "SENT"

    user = session.query(User).get(user_id)
    user.email = fake.email()
    user.username = fake.slug()
    user.first_name = fake.first_name()
    user.last_name = fake.last_name()

    session.commit()


def delete():
    session = Session()

    user_id = users.pop(0)  # Remove and get the first user from the list

    for notif in session.query(Notification).filter_by(user_id=user_id):
        session.delete(notif)

    user = session.query(User).get(user_id)
    session.delete(user)

    session.commit()


# ... Remaining code (like the main function) stays the same.
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
