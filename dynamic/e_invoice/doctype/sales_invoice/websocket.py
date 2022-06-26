#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
from email import message
import json
import logging
import re
import websockets
import os
import subprocess
logging.basicConfig()

STATE = {"value": 0}

USERS = set()


def invoice_post(data):

    # try :
    if 1:
        doc = data
        json_response = ""
        try:
            os.remove('C:/j/sFile.txt')
        except:
            pass
        jsonfile = "C:/j/sFile.txt"
        with open(jsonfile, 'a', encoding='utf-8') as outfile:
            json.dump(doc, outfile)
        cmd = 'C:/j/EInvoicingSigner.exe'
        result = subprocess.Popen(
            [cmd, ' '], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        a, b = result.communicate()
        print(a)
        print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
        print(b)
        json_response = a.decode('utf-8')

    # except :
    #    print("unable to load" , data)
    print("OK")
    return json.dumps({"status": "success", "response": json_response})


def state_event():
    return json.dumps({"type": "state", **STATE})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


def connct_event():

    return json.dumps({"status": "Token connecting"})


async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_connect():
    message = connct_event()
    await asyncio.wait([user.send(message) for user in USERS])


async def clear_user():

    USERS = set()


async def register(websocket):
    if len(USERS) == 0:
        USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


async def send_invoice(data):
    #print("Data" ,data[0])
    message = invoice_post(data)
    await asyncio.wait([user.send(message) for user in USERS])


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        #print("heelo Send")
        # await websocket.send("hello")
        #print("heelo Send2")

        async for message in websocket:
            data = json.loads(message)
            print("data ====>   ", data)
            print(type(data))
            if data.get("name"):
                await notify_connect()
                await clear_user()
            if data.get('documents'):
                await send_invoice(data.get("documents")[0])
                await clear_user()
            elif data.get("action") == "minus":
                STATE["value"] -= 1
                await notify_state()
            elif data.get("action") == "plus":
                STATE["value"] += 1
                await notify_state()
            else:
                logging.error("unsupported event: %s", data)
    finally:
        await unregister(websocket)


start_server = websockets.serve(counter, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
