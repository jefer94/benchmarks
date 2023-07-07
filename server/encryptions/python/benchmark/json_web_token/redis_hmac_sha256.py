

import base64
from datetime import datetime, timedelta
import os
import random
import jwt
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
    user = headers.get('User')
    payload = {
        'user_id': user,
        'exp': datetime.utcnow() + timedelta(minutes=30),
    }

    token = r.get(f'{path}:{rand}:service1:token:{user}')
    if not token:
        token = jwt.encode(payload, private_key, algorithm="HS256")
        r.set(f'{path}:{rand}:service1:token:{user}', token, timedelta(minutes=30))

    service2(body, {**headers, 'Authorization': f'Token {token}'}, query_params)
    return {'status': 'ok'}, {}


def service2(body={}, headers={}, query_params={}):
    user = headers.get('User')
    token = headers.pop('Authorization', None).replace('Token ', '')

    try:
        obj = r.hgetall(f'{path}:{rand}:service2:token:{user}')
        if not obj:
            obj = jwt.decode(token, private_key, algorithms=["HS256"])
            r.hset(f'{path}:{rand}:service2:token:{user}', mapping=obj)

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

    global rand
    global r

    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    rand = random.randint(10000000, 99999999)

def down(s):
    global r
    r.flushall()
    r.close()
