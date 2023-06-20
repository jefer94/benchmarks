
import hashlib
import hmac
import requests
from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS

app = Sanic("Service1")
CORS(app, origins='*')


@app.post("/")
async def hello_world(request):
    requests.post("http://localhost:4000/", json=request.json)
    return json({"id": 1})


@app.get("/shutdown")
async def shutdown(request):
    app.stop()
    return json({"status": "ok"})



