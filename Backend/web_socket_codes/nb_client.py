import asyncio
import websockets
from aioconsole import ainput  # Import aioconsole for non-blocking input

async def client():
    uri = "ws://localhost:6789"
    async with websockets.connect(uri) as websocket:
        message_queue = asyncio.Queue()

        async def simulate_input():
            while True:
                message = await ainput("Msg to server: ")  # Non-blocking input
                await message_queue.put(message)

        async def send_messages():
            while True:
                message = await message_queue.get()
                await websocket.send(message)
                print(f"Client sent: {message}")

        async def receive_messages():
            async for message in websocket:
                print(f"Server: {message}")

        await asyncio.gather(simulate_input(), send_messages(), receive_messages())

asyncio.get_event_loop().run_until_complete(client())