import asyncio
from websockets.sync.client import connect

def hello():
    with connect("ws://localhost:8765") as websocket:
        text = input("1 to send 2 to recv")
        if text == "1":
            websocket.send("registration|vlad3|1020315s2")
            print(websocket.recv())
        if text == "2":
            print(websocket.recv())
        input()
hello()