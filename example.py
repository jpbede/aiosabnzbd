import asyncio
import pprint

import aiosabnzbd


async def main():
    async with aiosabnzbd.SABnzbd(
        host="homeassistant.local",
        port=8082,
        api_key="b61365cda9234f599db2dc9e668debab",
    ) as client:
        pprint.pprint(await client.queue())


asyncio.run(main())
