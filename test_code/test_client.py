import asyncio
from websockets.sync.client import connect

def hello():
    with connect("ws://localhost:8765") as websocket:
        websocket.send("login|step5an".encode("utf-16"))
        while True:
            message = websocket.recv()
            print(f"Received: {message}")
        websocket.send(bytes)

hello()