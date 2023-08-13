

from datetime import datetime, timedelta
import random
import jwt
import base64

from benchmark import generators

with open(".ed25519.public_key.pem", "rb") as f:
    public_key = f.read()


with open(".ed25519.private_key.pem", "rb") as f:
    private_key = f.read()


def service1(body={}, headers={}, query_params={}):
    payload = {
        'user_id': headers.get('User'),
        'exp': datetime.utcnow() + timedelta(minutes=30),
    }
    token = jwt.encode(payload, private_key, algorithm="PS256")

    service2(body, {**headers, 'Authorization': f'Token {token}'}, query_params)
    return {'status': 'ok'}, {}


def service2(body={}, headers={}, query_params={}):
    token = headers.pop('Authorization', None).replace('Token ', '')

    try:
        jwt.decode(token, private_key, algorithms=["PS256"])

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