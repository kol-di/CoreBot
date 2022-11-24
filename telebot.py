from telethon import TelegramClient, events
from configparser import ConfigParser
import logging


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

config = ConfigParser()
config.read("config.ini")

telegram_config = config['Telethon']
API_ID = int(telegram_config['api_id'])
API_HASH = telegram_config['api_hash']

client = TelegramClient('bot', API_ID, API_HASH)
client.start()


async def coreify_context(event):
    sender = await event.get_sender()
    async with client.conversation(sender.id, exclusive=False) as conv:
        # await event.respond('Let me look at your picture')
        await conv.send_message('Let me look at your picture')
        next_msg = await conv.get_response()
        await conv.send_message('nice!')



@client.on(events.NewMessage(pattern=r'/.*'))
async def my_event_handler(event):
    match event.raw_text:
        case '/which':
            await coreify_context(event)


# async def startup():
#     me = await client.get_me()
#     await client.send_message(me, 'Hi')
#     print(me.username)
#
#
# with client:
#     client.loop.run_until_complete(startup())

client.run_until_disconnected()


