#!/usr/bin/env python3

import os
import secrets
import asyncio
import aiofiles


DATA_DIRECTORY = '/var/tmp/data/'
SECRET_FILENAME = '/var/local/secret.txt'


async def main():
    async with aiofiles.open(SECRET_FILENAME, 'r') as file:
        secret = await file.read()

    filename = secrets.token_hex(8)
    secret_path = os.path.join(DATA_DIRECTORY, filename)

    async with aiofiles.open(secret_path, 'w') as file:
        await file.write(secret)

    await asyncio.sleep(1)

    os.unlink(secret_path)

    return


if __name__ == '__main__':
    asyncio.run(main())
