import random
from time import time
import urllib.parse
import hashlib
import hmac
from .. import generators


with open(".ed25519.public_key.pem", "rb") as f:
    public_key = f.read()


with open(".ed25519.private_key.pem", "rb") as f:
    private_key = f.read()

def service1(body={}, headers={}, query_params={}):
    body = {
        **body,
        'user_id': headers.get('User'),
    }

    headers = {
        **headers,
        'Timestamp': f'{time()}',
    }

    payload = {
        'body': body,
        'headers': headers,
        'query_params': query_params,
    }

    paybytes = urllib.parse.urlencode(payload).encode('utf8')

    sign = hmac.new(private_key, paybytes, hashlib.sha512).hexdigest()

    headers = {
        **headers,
        'Authorization': f'Signature {sign}',
    }
    service2(body, headers, query_params)
    return {'status': 'ok'}, {}


def service2(body={}, headers={}, query_params={}):
    token = headers.pop('Authorization', None).replace('Signature ', '')

    payload = {
        'body': body,
        'headers': headers,
        'query_params': query_params,
    }
    
    paybytes = urllib.parse.urlencode(payload).encode('utf8')

    sign = hmac.new(private_key, paybytes, hashlib.sha512).hexdigest()

    if not hmac.compare_digest(sign, token):
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
