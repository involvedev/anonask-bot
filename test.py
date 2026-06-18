import asyncio

asyncio.set_event_loop_policy(
    asyncio.WindowsSelectorEventLoopPolicy()
)

import aiohttp

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.telegram.org") as r:
            print(r.status)

asyncio.run(main())