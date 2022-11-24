import asyncio.exceptions

from telethon import TelegramClient, events
from configparser import ConfigParser
import logging
import os


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

config = ConfigParser()
config.read("config.ini")

telegram_config = config['Telethon']
API_ID = int(telegram_config['api_id'])
API_HASH = telegram_config['api_hash']

client = TelegramClient('bot', API_ID, API_HASH)
client.start()


async def break_chat_context(event):
    sender_id = event.sender_id
    async with client.conversation(sender_id, exclusive=False) as conv:
        await conv.cancel_all()


async def coreify_context(event):
    sender_id = event.sender_id
    async with client.conversation(sender_id, exclusive=False) as conv:
        await conv.send_message('Let me look at your picture')
        try:
            while True:
                resp_msg = await conv.get_response()
                if resp_msg.photo is not None:
                    await conv.send_message('cool pic!')
                    await conv.send_file(resp_msg.photo)
                    save_dir = os.path.join(os.getcwd(), "photo")
                    await client.download_media(resp_msg.photo, save_dir)
                    return
                else:
                    await conv.send_message('send an image or call /cancel')
        except asyncio.exceptions.TimeoutError:
            await conv.send_message("Session expired")
            await break_chat_context(event)


@client.on(events.NewMessage(pattern=r'/.*'))
async def my_event_handler(event):
    match event.raw_text:
        case '/which':
            await coreify_context(event)
        case '/cancel':
            await break_chat_context(event)


client.run_until_disconnected()


