import math
import timeit
import pandas as pd

from . import json_web_token
from . import signature
from . import nothing

HOW_MANY = 500

def calculate(module, s):
    if hasattr(module, 'up'):
        module.up(s)
    
    fn = getattr(module, s)
    l = timeit.repeat(fn, number=HOW_MANY)

    if hasattr(module, 'down'):
        module.down(s)

    n = len(l)
    res = sum(l) / n
    return res


def run(s):
    result = []

    def append(*args):
        result.append([*args])

    print()
    print(f"Running {s} benchmark ({HOW_MANY} iterations)")

    # Base
    append(None, None, "Nothing", "Native", calculate(nothing, s))

    base = result[0][-1]

    # Json Web Token
    append(None, "ED25519 SHA512", "JWT", "PyJWT", calculate(json_web_token.ed25519_sha512, s))
    append(None, "HMAC SHA256", "JWT", "PyJWT", calculate(json_web_token.hmac_sha256, s))
    append(None, "HMAC SHA512", "JWT", "PyJWT", calculate(json_web_token.hmac_sha512, s))
    # append(None, "ECDSA SHA256", "JWT", "PyJWT", calculate(json_web_token.ecdsa_sha256, s))
    # append(None, "RSASSA-PSS SHA256", "JWT", "PyJWT", calculate(json_web_token.rsassa_pss_sha512, s))

    # Json Web Token with database
    append('Redis', "HMAC SHA256", "JWT", "PyJWT", calculate(json_web_token.redis_hmac_sha256, s))
    append('MongoDB', "HMAC SHA256", "JWT", "PyJWT", calculate(json_web_token.mongo_hmac_sha256, s))
    append('MongoDB', "HMAC SHA512", "JWT", "PyJWT", calculate(json_web_token.mongo_hmac_sha512, s))
    append('Postgres', "HMAC SHA256", "JWT", "PyJWT", calculate(json_web_token.postgres_hmac_sha256, s))
    append('Postgres', "HMAC SHA512", "JWT", "PyJWT", calculate(json_web_token.postgres_hmac_sha512, s))
    append('Cache', "HMAC SHA256", "JWT", "Native", calculate(json_web_token.cache_hmac_sha256, s))
    append('Cache', "HMAC SHA512", "JWT", "Native", calculate(json_web_token.cache_hmac_sha512, s))

    # # Signature
    # append(None, "ED25519", "Signature", "ed25519", calculate(signature.ed25519, s))
    append(None, "HMAC SHA256", "Signature", "Native", calculate(signature.hmac_sha256, s))
    append(None, "HMAC SHA512", "Signature", "Native", calculate(signature.hmac_sha512, s))

    result = [[*r, r[-1] - base, round(r[-1] / base * 100), round(1 / r[-1] * HOW_MANY)] for r in result]
    # result = [[*r, r[-2] / base] for r in result]
    headers=[
        "Database", "Algoritm", "Technologie", "Implementation",  "Result(s)", "Delta(s)", "%", "Requests/s"
    ]
    print(pd.DataFrame(result, columns= headers).sort_values(by="Delta(s)", ascending=True))

print("Benchmarking...")
print("Short len(rand_obj) == 3, Medium len(rand_obj) == 10 and Big len(rand_obj) == 30")

run("short")
run("medium")
run("big")