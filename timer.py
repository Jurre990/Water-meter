import asyncio
import websockets
import time
import shelve

async def timer(websocket, path):
    print("test")
    now_time = time.time()
    start_time = time.time()
    elapsed_time = 0
    running = False
    with shelve.open("/home/pi/Desktop/timer") as db:
        showerTime = db.get("showerTime")
        if db.get("start_time") != None:
            start_time = db.get("start_time")
        else:
            db["start_time"] = start_time
        if db.get("elapsed_time") != None:
            elapsed_time = db.get("elapsed_time")
        else:
            db["elapsed_time"] = elapsed_time
        if db.get("running") != None:
            running = db.get("running")
        else:
            db["running"] = running
    try:
        if running:
            await websocket.send("stillRunning")
        async for message in websocket:
            if not websocket.open or message == "stop":
                break
            if message == "true" and not running:
                now_time = time.time()
                start_time = time.time()
                running = True
                with shelve.open("/home/pi/Desktop/timer") as db:
                    db["start_time"] = start_time
                    db["running"] = running
            elif message == "true":
                now_time = time.time()
            elif running:
                running = False
                elapsed_time += now_time - start_time  # type: ignore
                with shelve.open("/home/pi/Desktop/timer") as db:
                    db["elapsed_time"] = elapsed_time
                    db["running"] = running
            if running:
                print("running")
                if showerTime - (now_time - start_time + elapsed_time) > 0:
                    await websocket.send(str(round((showerTime - (now_time - start_time + elapsed_time)) * 1000)))  # type: ignore
                else:
                    await websocket.send("0")
            else:
                if showerTime - (now_time - start_time + elapsed_time) > 0:
                    await websocket.send(str(round((showerTime - elapsed_time) * 1000)))  # type: ignore
                else:
                    await websocket.send("0")
            if message == 'reset':
                now_time = time.time()
                start_time = time.time()
                elapsed_time = 0
                with shelve.open("/home/pi/Desktop/timer") as db:
                    db["elapsed_time"] = elapsed_time
                    db["start_time"] = start_time
            await asyncio.sleep(0.01)
    except:
        pass

if __name__ == "__main__":
    try:
        start_server = websockets.serve(timer, "0.0.0.0", 5678, ping_interval=None)  # type: ignore
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except:
        pass
