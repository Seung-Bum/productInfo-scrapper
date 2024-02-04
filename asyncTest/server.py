import asyncio
import websockets


async def handler(websocket, path):
    for i in range(1, 11):  # 1부터 10까지의 숫자를 클라이언트로 보냄
        await websocket.send(str(i))
        await asyncio.sleep(1)  # 1초 동안 대기

start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
