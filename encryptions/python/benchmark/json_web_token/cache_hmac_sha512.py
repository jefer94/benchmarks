

import base64
from datetime import datetime, timedelta
from functools import cache, lru_cache
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


@lru_cache(maxsize=128)
def get_token(user):
    payload = {
        'user_id': user,
        'exp': datetime.utcnow() + timedelta(minutes=30),
    }

    return jwt.encode(payload, private_key, algorithm="HS512")

@lru_cache(maxsize=128)
def is_valid_token(token):
    try:
        return jwt.decode(token, private_key, algorithms=["HS512"])
    
    except:
        return None


def service1(body={}, headers={}, query_params={}):
    user = headers.get('User')
    token = get_token(user)

    service2(body, {**headers, 'Authorization': f'Token {token}'}, query_params)
    return {'status': 'ok'}, {}


def service2(body={}, headers={}, query_params={}):
    user = headers.get('User')
    token = headers.pop('Authorization', None).replace('Token ', '')

    if not is_valid_token(token):
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

    get_token.cache_clear()
