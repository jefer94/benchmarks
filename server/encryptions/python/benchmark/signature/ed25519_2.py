import base64
import json
import random
import time
import nacl.utils
from nacl.public import PrivateKey, Box
from nacl.signing import SigningKey

from benchmark import generators

with open(".ed25519.public_key", "rb") as f:
    public_key = f.read()


with open(".ed25519.private_key", "rb") as f:
    private_key = f.read()


def service1(body={}, headers={}, query_params={}):
    body = {
        **body,
        'user_id': headers.get('User'),
    }

    headers = {
        **headers,
        'Timestamp': f'{time.time()}',
    }

    payload = {
        'body': body,
        'headers': headers,
        'query_params': query_params,
    }

    import ed25519

    privKey = ed25519.SigningKey(private_key)

    message = json.dumps(payload).encode()
    signature = privKey.sign(message)
    signature = base64.b64encode(signature[:64])

    headers = {
        **headers,
        'Authorization': f'Signature {signature}',
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

    message = json.dumps(payload).encode()
    import ed25519
    pubKey = ed25519.VerifyingKey(public_key)
    # token.decode("ascii")
    # print('token', base64.b64decode(token))
    # token = base64.b64decode(token)
    token = base64.b64encode(bytes(token))

    try:
        pubKey.verify(token, message, encoding='base64')

    except Exception as e:
        import traceback
        traceback.print_exc()
        print('error in service 2', __file__, e)
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
