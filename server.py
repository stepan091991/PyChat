import asyncio

import websockets
from websockets.server import serve
import data_base
connected = set()
async def echo(websocket):
    connected.add(websocket)
    async for message in websocket:
        data = message.split("|")
        if data[0] == "registration":
            await websocket.send(data_base.registration(data[1],data[2]))
        elif data[0] == "login":
            await websocket.send(data_base.login(data[1],data[2]))
        elif data[0] == "message":
            websockets.broadcast(connected, message)
            pass
        elif data[0] == "none":
            pass

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())