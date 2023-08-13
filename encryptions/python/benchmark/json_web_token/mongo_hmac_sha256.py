

import base64
from datetime import datetime, timedelta
import os
import random
import jwt
from pymongo import MongoClient
import redis

from benchmark import generators

path = os.path.dirname(__file__)
rand = random.randint(10000000, 99999999)

with open(".ed25519.public_key.pem", "rb") as f:
    public_key = f.read()
    public_key = base64.b64encode(public_key)


with open(".ed25519.private_key.pem", "rb") as f:
    private_key = f.read()
    private_key = base64.b64encode(private_key)


def service1(body={}, headers={}, query_params={}):
    global db
    global rand

    user = headers.get('User')
    now = datetime.utcnow()
    payload = {
        'user_id': user,
        'exp': now + timedelta(minutes=30),
    }

    obj = db.tokens.find_one({"user": user, "rand": rand, "exp": {"$gt": now}})
    if obj:
        token = obj['token']

    else:
        token = jwt.encode(payload, private_key, algorithm="HS256")
        db.tokens.insert_one({
            "user": user,
            "exp": payload['exp'],
            "token": token,
            "rand": rand,
        })

    service2(body, {**headers, 'Authorization': f'Token {token}'}, query_params)
    return {'status': 'ok'}, {}


def service2(body={}, headers={}, query_params={}):
    global rand

    user = headers.get('User')
    token = headers.pop('Authorization', None).replace('Token ', '')
    now = datetime.utcnow()

    try:
        obj = db.tokens.find_one({"user": user, "rand": rand, "exp": {"$gt": now}})
        if obj:
            token = obj['token']

        else:
            obj = jwt.decode(token, private_key, algorithms=["HS256"])

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
    global shorts
    global mediums
    global bigs

    if s == 'short':
        shorts = [generators.short_object_generator() for _ in range(2500)]
    
    elif s == 'medium':
        mediums = [generators.medium_object_generator() for _ in range(2500)]

    elif s == 'big':
        bigs = [generators.big_object_generator() for _ in range(2500)]

    global client
    global db
    global rand

    CONNECTION_STRING = "mongodb://root:example@localhost:27017"
    client = MongoClient(CONNECTION_STRING)

    db =  client['benchmarks']
    rand = random.randint(10000000, 99999999)


def down(s):
    global client
    client.close()
