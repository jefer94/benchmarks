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


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Integer)


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    kind = Column(String)
    external_id = Column(Integer, ForeignKey("products.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    not_before = Column(DateTime)
    expires_at = Column(DateTime)
    subject = Column(String)
    message = Column(String)
    status = Column(String)


def setup():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def insert():
    session = Session()
    user = User(
        email=fake.email(), username=fake.slug(), first_name=fake.first_name(), last_name=fake.last_name()
    )
    session.add(user)
    session.flush()

    for _ in range(ACTIVITIES):
        product = Product(name="John Doe", amount=100)
        session.add(product)
        session.flush()

        expires_at = timedelta(days=1, hours=2, minutes=30, seconds=0)
        not_before = timedelta(days=0, hours=2, minutes=30, seconds=0)

        notification = Notification(
            kind="PRODUCT",
            external_id=product.id,
            user_id=user.id,
            not_before=datetime.utcnow() + not_before,
            expires_at=datetime.utcnow() + expires_at,
            subject="Your product is ready",
            message="Your product is ready to be picked up",
            status="NEW",
        )
        session.add(notification)

    session.commit()
    session.close()


def select():
    session = Session()
    for user in session.query(User).all():
        for notification in session.query(Notification).filter_by(user_id=user.id).all():
            pass  # Do something with the notification if needed
    session.close()


def update():
    session = Session()
    for user in session.query(User).all():
        user.email = fake.email()
        user.username = fake.slug()
        user.first_name = fake.first_name()
        user.last_name = fake.last_name()

        for notification in session.query(Notification).filter_by(user_id=user.id).all():
            notification.status = "SENT"

    session.commit()
    session.close()


def delete():
    session = Session()
    for user in session.query(User).all():
        for notification in session.query(Notification).filter_by(user_id=user.id).all():
            session.delete(notification)
        session.delete(user)

    session.commit()
    session.close()


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
