from datetime import datetime
import hashlib
import requests
from sanic import Sanic
from sanic.response import json
from sanic import Request, Websocket
from sanic_cors import CORS
import hmac
import json as js

app = Sanic("Service2")
CORS(app, origins='*')


with open('../../../id_rsa', 'r') as f:
    PRIVATE = f.read()


@app.post("/")
async def report(request: Request):
    message = js.dumps(request.json)
    
    hmac.new(PRIVATE.encode('latin-1'), message.encode('latin-1'), hashlib.sha512).hexdigest()
    
    requests.post("http://localhost:5000/result", json=request.json)
    return json({"status": "ok"})



@app.get("/shutdown")
async def shutdown(request):
    app.stop()
    return json({"status": "ok"})

