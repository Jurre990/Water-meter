#!/usr/bin/env python3
import asyncio
import websockets
import time

start_time = time.time()
now_time = time.time()
elapsed_time = 0
running = False

async def timer(websocket, path):
    global start_time
    global now_time
    global elapsed_time
    global running
    if running:
        await websocket.send("stillRunning")
    try:
        async for message in websocket:
            if not websocket.open:
                break
            if message == "true" and not running:
                now_time = time.time()
                start_time = time.time()
                running = True
            elif message == "true":
                now_time = time.time()
            elif running:
                running = False
                elapsed_time += now_time - start_time
            if running:
                await websocket.send(str(round((now_time - start_time + elapsed_time) * 1000)))
            else:
                await websocket.send(str(round((elapsed_time) * 1000)))
            if message == 'reset':
                now_time = time.time()
                start_time = time.time()
                elapsed_time = 0
            await asyncio.sleep(0.01)
    except:
        pass

if __name__ == "__main__":
    start_server = websockets.serve(timer, "0.0.0.0", 5678, ping_interval=None)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()