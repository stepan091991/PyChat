import asyncio
import rsa
import websockets
from websockets.server import serve
from server import data_base

#message|name|public or private|receiver_name|message_text
(my_pub_key, my_priv_key) = rsa.newkeys(2048)
print(my_pub_key)
client_pub_key = None
connected = set()
client_keys = {}
users = {}
async def echo(websocket):
    connected.add(websocket)
    try:
        async for message in websocket:
            print(f"Получено зашифрованое сообщение:{message}")
            def encript(text,user_):
                return rsa.encrypt(text.encode("utf8"), rsa.PublicKey(int(client_keys.get(user_).split("|")[0]), int(client_keys.get(user_).split("|")[1])))
            if type(message) == str:
                if message.split("|")[0] == "key":
                    client_keys.update({websocket:f'{int(message.split("|")[1])}|{int(message.split("|")[2])}'})
                    await websocket.send(f"key|{my_pub_key.n}|{my_pub_key.e}")
            if type(message) == bytes:
                data_decript = rsa.decrypt(message, my_priv_key)
                print(f"Сообщение расшифровано:{data_decript.decode('utf8')}")
                data = data_decript.decode("utf8").split("|")
                if data[0] == "registration":
                    await websocket.send(encript(data_base.registration(data[1], data[2]), websocket))
                elif data[0] == "login":
                    await websocket.send(encript(data_base.login(data[1], data[2]), websocket))
                    if data_base.login(data[1], data[2]) == "login_info|yes|none":
                        users.update({websocket: data[1]})
                elif data[0] == "message":
                    if data[2] == "public":
                        for user in connected:
                            await user.send(encript(data_decript.decode("utf8"),user))
                    pass
                elif data[0] == "none":
                    pass
    except websockets.ConnectionClosedOK:
        pass
    except websockets.ConnectionClosedError:
        connected.remove(websocket)
        client_keys.pop(websocket)
async def main():
    async with serve(echo, "192.168.0.102", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())