import asyncio.exceptions
from telethon import TelegramClient, events
from configparser import ConfigParser
import os
import uuid

from classifier import get_core_model


config = ConfigParser()
config.read("config.ini")
telegram_config = config['Telethon']

API_ID = int(telegram_config['api_id'])
API_HASH = telegram_config['api_hash']
BOT_TOKEN = telegram_config['bot_token']

IMAGE_SAVE_PATH = config['Files']['IMAGE_SAVE_PATH']


async def start_client():
    if not os.path.exists(IMAGE_SAVE_PATH):
        os.makedirs(IMAGE_SAVE_PATH)
    client = TelegramClient('bot', API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)
    return client


async def client_main_loop(client):
    model = get_core_model()

    async def break_chat_context(event):
        sender_id = event.sender_id
        async with client.conversation(sender_id, exclusive=False) as conv:
            await conv.cancel_all()

    async def which_core_context(event):
        sender_id = event.sender_id
        async with client.conversation(sender_id, exclusive=False) as conv:
            await conv.send_message('Let me look at your picture')
            try:
                while True:
                    resp_msg = await conv.get_response()
                    if resp_msg.photo is not None:
                        await conv.send_message('cool pic!')
                        img_file_name = f'{IMAGE_SAVE_PATH}/{uuid.uuid4().hex}'
                        await resp_msg.download_media(img_file_name)
                        await conv.send_message(model(img_file_name))
                        return
                    else:
                        await conv.send_message('send an image or call /cancel')
            except asyncio.exceptions.TimeoutError:
                await conv.send_message("Session expired")
                await break_chat_context(event)

    @client.on(events.NewMessage(pattern=r'/.*'))
    async def event_handler(event):
        match event.raw_text:
            case '/which':
                await which_core_context(event)
            case '/cancel':
                await break_chat_context(event)

    await client.run_until_disconnected()
