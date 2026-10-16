import asyncio
import sys

import websockets
from loguru import logger


async def main(session_uid: str, text: str) -> None:
    url = f"ws://localhost:5000/ws/normal_chat/{session_uid}"
    async with websockets.connect(url) as ws:
        await ws.send(text)
        async for message in ws:
            logger.info(message)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "hello"))
