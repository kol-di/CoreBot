import logging
import asyncio
from configparser import ConfigParser
import argparse

from classifier import create_core_model
from telebot import start_client, client_main_loop


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--save-images', action='store_true', default=False)
    args = parser.parse_args()
    return vars(args)


async def main():
    args = parse_args()
    save_images = args['save_images']

    config = ConfigParser()
    config.read("config.ini")
    state_dict_path = config['Files']['STATE_DICT_PATH']

    _, client = await asyncio.gather(
        create_core_model(state_dict_path),
        start_client()
    )
    logging.log(100, 'Client launched')
    await client_main_loop(client, save_images)
    logging.log(100, 'Client exited')
    return client


if __name__ == '__main__':
    logging.basicConfig(filename='app.log',
                        format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                        level=logging.WARNING)

    asyncio.run(main())
