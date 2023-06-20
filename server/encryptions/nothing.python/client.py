import asyncio
from io import StringIO
import os
import time
import pandas as pd
from sanic import Sanic
from sanic.response import json
from datetime import datetime, timedelta
from threading import Thread
from sanic import Request, Websocket
from sanic_cors import CORS


import requests

app = Sanic("Client")
CORS(app, origins='*')

START = datetime.utcnow()

@app.post("/result")
async def result(request: Request):
    return json({"status": "ok"})

id = 0

def worker(alias):
    global id
    global START

    results = {}

    time.sleep(2)

    ends_at = datetime.utcnow() + timedelta(seconds=10)
    while True:
        now = datetime.utcnow()
        if now > ends_at:
            break

        start = datetime.utcnow()
        key = f"{alias}-{id}"

        try:
            requests.post("http://localhost:3000/", json={"id": id, "worker": alias, "name": "Alice",})
        except:
            break

        end = datetime.utcnow()

        ms = (end - start).total_seconds() * 1000

        results[key] = {"key": key, "start": start, "end": end, "ms": ms}

        id += 1

    content = "".join([f"{v['key']},{v['start']},{v['end']},{v['ms']}\n" for v in results.values()])


    with open("results.csv", "a") as f:
        f.write(content)

    try:
        requests.get("http://localhost:3000/shutdown")
    except:
        pass



def killer():
    delta = (START + timedelta(seconds=13)) - datetime.utcnow()
    time.sleep(delta.seconds)
            
    try:
        requests.get("http://localhost:4000/shutdown")
    except:
        pass

    with open("results.csv", "r") as f:
        df = pd.read_csv(f, sep=",")

    mode = df['ms'].mode()
    mean = df['ms'].mean()
    median = df['ms'].median()
    min = df['ms'].min()
    max = df['ms'].max()
    count = df['ms'].count()


    output = '\n'.join([
        '',
        'summary',
        '',
        "- Mean: " + str(mean) + "ms",
        "- Median: " + str(median) + "ms",
        "- Min: " + str(min) + "ms",
        "- Max: " + str(max) + "ms",
        '',
        "About "+ str(count / 10) + " requests per second",
        ''
    ])

    print(output)

    with open("../../../results.md", "a") as f:
        f.write("## No encryption\n" + output + "\n\n")

    # try:
    #     app.stop()
    # except:
    #     ...

    # exit(0)


@app.main_process_start
async def my_task(app, loop):
    global START

    with open("results.csv", "w") as f:
        f.write("key,start,end,ms\n")

   
    
    START = datetime.utcnow()
    for n in range(int(os.getenv('WORKERS'))):
        processThread = Thread(target=worker, args=(n,))  # <- note extra ','
        processThread.start()


    processThread = Thread(target=killer)  # <- note extra ','
    processThread.start()
