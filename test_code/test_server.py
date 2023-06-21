import asyncio
import websockets
from websockets.server import serve
import rsa
(bob_pub, bob_priv) = rsa.newkeys(1024)
#message|name|public or private|receiver_name|message_text
users = {}
connected = set()
async def echo(websocket):
    try:
        connected.add(websocket)
        async for message in websocket:
            print(message)
            data = message.decode("utf-16").split("|")
            print(message.decode("utf-16"))
            if data[0] == "login":
                websocket.send("")
                users.update({websocket:data[1]})
    except websockets.ConnectionClosedError as err:
        connected.remove(websocket)
        users.pop(websocket)
    def crypt(text):
        return rsa.encrypt(message, bob_pub)
async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())