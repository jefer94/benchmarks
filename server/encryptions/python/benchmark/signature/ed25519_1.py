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

    from nacl.encoding import HexEncoder, RawEncoder, Base64Encoder
    from nacl.signing import VerifyKey

    signing_key = SigningKey(private_key)
    message = json.dumps(payload).encode()
    signednonce = signing_key.sign(message, encoder=HexEncoder)
    # signed_hex = signing_key.sign(b"Attack at Dawn", encoder=HexEncoder)
    print(signednonce)

    # verify_key = signednonce.verify_key
    # verify_key_hex = verify_key.encode(encoder=HexEncoder)


    # print(len(signednonce[:64]))
    # sign = signednonce.hex()
    sign = signednonce[:64].hex()
    # sign = signednonce[:64].base64()
    # sign = signednonce[:64].decode('ascii')
    # sign = base64.b64encode(signednonce[:64])
    # sign = binascii.b2a_hex(signednonce[:64])
    # print(0, signednonce[:64])

    # sign = signednonce

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
    
    from nacl.encoding import HexEncoder, RawEncoder, Base64Encoder
    from nacl.signing import VerifyKey

    # Create a VerifyKey object from a hex serialized public key
    # signingkey = SigningKey(public_key)
    # print(11111,len(bytes(token, 'ascii')))
    print(11111, token)
    verify_key = VerifyKey(public_key)

    # Check the validity of a message's signature
    # The message and the signature can either be passed together, or
    # separately if the signature is decoded to raw bytes.
    # These are equivalent:
    # verify_key.verify(signed_hex, encoder=HexEncoder)
    # signature_bytes = HexEncoder.decode(signed_hex.signature)
    message = json.dumps(payload).encode()
    print(22222, token)
    # signature_bytes = HexEncoder.decode(token.strip())
    # signature_bytes = Base64Encoder.decode(token)
    # signature_bytes = token.encode('ascii')
    signature_bytes = base64.b64decode(token)
    print(33333, signature_bytes)

    # print(33333, signature_bytes)

    # verify_key.verify(signature_bytes, encoder=RawEncoder)
    # verify_key.verify(message, signature_bytes, encoder=RawEncoder)

    # Alter the signed message text
    forged = signature_bytes[:-1] + bytes([int(signature_bytes[-1]) ^ 1])
    # Will raise nacl.exceptions.BadSignatureError, since the signature check
    # is failing
    verify_key.verify(forged)

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
