

import base64
from datetime import datetime, timedelta
import os
import random
import jwt
from pymongo import MongoClient
from sqlalchemy import Column, create_engine
from sqlalchemy.orm import Session

from benchmark import generators

path = os.path.dirname(__file__)
rand = random.randint(10000000, 99999999)
# dsn := "host=localhost user=postgres password=postgres dbname=postgres port=5432 sslmode=disable TimeZone=Asia/Shanghai"

from typing import List
from typing import Optional
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Token(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(Integer())
    exp: Mapped[datetime] = Column(DateTime())
    token: Mapped[str] = Column(String())
    rand: Mapped[int] = Column(String())

    def __repr__(self) -> str:
        return 

with open(".ed25519.public_key.pem", "rb") as f:
    public_key = f.read()
    public_key = base64.b64encode(public_key)


with open(".ed25519.private_key.pem", "rb") as f:
    private_key = f.read()
    private_key = base64.b64encode(private_key)


def service1(body={}, headers={}, query_params={}):
    global engine
    global rand

    user = headers.get('User')
    now = datetime.utcnow()
    payload = {
        'user_id': user,
        'exp': now + timedelta(minutes=30),
    }

    with Session(engine) as session:
        # delete all rows in the tokens table
        obj = session.query(Token).filter(Token.user == user, Token.rand == rand, Token.exp > now).first()

        if obj:
            token = obj.token

        else:
            token = jwt.encode(payload, private_key, algorithm="HS512")

            t = Token(
                user= user,
                exp= payload['exp'],
                token= token,
                rand= rand,
            )
            session.add(t)
            session.commit()

    service2(body, {**headers, 'Authorization': f'Token {token}'}, query_params)
    return {'status': 'ok'}, {}


def service2(body={}, headers={}, query_params={}):
    global engine
    global rand

    user = headers.get('User')
    token = headers.pop('Authorization', None).replace('Token ', '')
    now = datetime.utcnow()

    try:
        with Session(engine) as session:
            # delete all rows in the tokens table
            obj = session.query(Token).filter(Token.user == user, Token.rand == rand, Token.exp > now).first()

            if obj:
                token = obj.token

            else:
                obj = jwt.decode(token, private_key, algorithms=["HS512"])

    except:
        print('error in service 2', __file__)
        return {'status': 'invalid'}, {}

    return {'status': 'ok'}, {}


def short():
    global shorts
    body = shorts.pop()
    headers = {
        'User': random.randint(1, 20),
    }
    service1(body, headers)

def medium():
    global mediums
    body = mediums.pop()
    headers = {
        'User': random.randint(1, 20),
    }
    service1(body, headers)

def big():
    global bigs
    body = bigs.pop()
    headers = {
        'User': random.randint(1, 20),
    }
    service1(body, headers)

def up(s):
    global engine
    global rand
    global shorts
    global mediums
    global bigs

    if s == 'short':
        shorts = [generators.short_object_generator() for _ in range(2500)]
    
    elif s == 'medium':
        mediums = [generators.medium_object_generator() for _ in range(2500)]

    elif s == 'big':
        bigs = [generators.big_object_generator() for _ in range(2500)]

    CONNECTION_STRING = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
    engine = create_engine(CONNECTION_STRING)

    rand = random.randint(10000000, 99999999)

    with Session(engine) as session:
        # delete all rows in the tokens table
        session.query(Token).delete()
        session.commit()


# def down(s):
#     global client
#     client.close()
