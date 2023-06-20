from datetime import datetime
import requests
from sanic import Sanic
from sanic.response import json
from sanic import Request, Websocket
from sanic_cors import CORS

app = Sanic("Service2")
CORS(app, origins='*')


# @app.middleware("auth")
# async def auth(request):
#     request.ctx.user = await extract_user_from_request(request)


# @app.websocket("/feed")
# async def feed(request: Request, ws: Websocket):
#     async for msg in ws:
#         await ws.send(msg)


@app.post("/")
async def report(request):
    requests.post("http://localhost:5000/result", json=request.json)
    return json({"status": "ok"})



@app.get("/shutdown")
async def shutdown(request):
    app.stop()
    return json({"status": "ok"})

