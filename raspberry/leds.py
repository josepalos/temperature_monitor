import asyncio
import websockets

WS_URL = "ws://localhost:8000/ws/notifications/"


async def parse_message(message):
    print(message)


async def main():
    async with websockets.connect(WS_URL) as ws:
        async for message in ws:
            await parse_message(message)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    main()
