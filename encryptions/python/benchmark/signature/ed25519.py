import base64
import json
import random
import time
import nacl.utils
from nacl.public import PrivateKey, Box
from nacl.signing import SigningKey
import binascii

from benchmark import generators

with open(".ed25519.public_key", "rb") as f:
    public_key = f.read()


with open(".ed25519.private_key", "rb") as f:
    private_key = f.read()


def service1(body={}, headers={}, query_params={}):
    body = {
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

    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    prk = Ed25519PrivateKey.from_private_bytes(private_key)
    message = json.dumps(payload).encode()
    signature = prk.sign(message)
    signature = base64.b64encode(signature)

    # public_key = private_key.public_key()
    # # Raises InvalidSignature if verification fails
    # public_key.verify(signature, b"my authenticated message")

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
    
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    puk = Ed25519PublicKey.from_public_bytes(public_key)
    message = json.dumps(payload).encode()

    token = base64.b64decode(token)

    signature = puk.verify(token, message)

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
