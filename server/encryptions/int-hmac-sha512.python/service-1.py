
from datetime import datetime
import hashlib
import hmac
import requests
from sanic import Request, Sanic
from sanic.response import json
from sanic_cors import CORS
import json as js

app = Sanic("Service1")
CORS(app, origins='*')


with open('../../../id_rsa', 'r') as f:
    PRIVATE = f.read()


@app.post("/")
async def hello_world(request: Request):
    API_SECRET = 'thekey'

    res = request.json
    res['nonce'] = datetime.utcnow().isoformat()

    message = js.dumps(res)

    signature = hmac.new(PRIVATE.encode('latin-1'), message.encode('latin-1'), hashlib.sha512) \
        .hexdigest()
    
    requests.post("http://localhost:4000/", json=request.json, headers={'apisign': signature})
    return json({"id": 1})


@app.get("/shutdown")
async def shutdown(request):
    app.stop()
    return json({"status": "ok"})



