import logging
import asyncio
from configparser import ConfigParser

from classifier import create_core_model
from telebot import start_client, client_main_loop


async def main():
    config = ConfigParser()
    config.read("config.ini")
    state_dict_path = config['Files']['STATE_DICT_PATH']

    _, client = await asyncio.gather(
        create_core_model(state_dict_path),
        start_client()
    )
    logging.log(100, 'Client launched')
    await client_main_loop(client)
    logging.log(100, 'Client exited')
    return client


if __name__ == '__main__':
    logging.basicConfig(filename='app.log',
                        format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                        level=logging.WARNING)

    asyncio.run(main())
