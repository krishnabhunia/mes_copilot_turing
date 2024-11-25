import asyncio
import websockets
from aioconsole import ainput  # Import aioconsole for non-blocking input

async def handler(websocket, path):
    message_queue = asyncio.Queue()

    async def simulate_input():
        while True:
            message = await ainput("Msg to client: ")  # Non-blocking input
            await message_queue.put(message)

    async def send_messages():
        while True:
            message = await message_queue.get()
            await websocket.send(message)
            print(f"Server sent: {message}")

    async def receive_messages():
        async for message in websocket:
            print(f"Client: {message}")

    await asyncio.gather(simulate_input(), send_messages(), receive_messages())

start_server = websockets.serve(handler, "localhost", 6789)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()