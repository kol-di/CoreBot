import asyncio.exceptions
import logging

from telethon import TelegramClient, events
import os
import uuid
import random
from enum import Enum, auto

from classifier import get_core_model
from utils import get_env_var


API_ID = get_env_var('API_ID')
API_HASH = get_env_var('API_HASH')
BOT_TOKEN = get_env_var('BOT_TOKEN')
IMAGE_SAVE_PATH = get_env_var('IMAGE_SAVE_PATH')


class ChatState(Enum):
    EXISTING_CONV = auto()


conversation_state = {}


async def start_client():
    if not os.path.exists(IMAGE_SAVE_PATH):
        os.makedirs(IMAGE_SAVE_PATH)
    client = TelegramClient('bot', API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)
    return client


async def client_main_loop(client, save_images):
    model = get_core_model()

    async def break_chat_context(event):
        sender_id = event.sender_id
        async with client.conversation(sender_id, exclusive=False) as conv:
            await conv.cancel_all()

    async def about_context(event):
        await break_chat_context(event)
        await event.respond(
            "This bot was trained to distinguish between 4 aesthetic genres, namely Draincore, Glitchcore, "
            "Weirdcore and Breakcore, no Lesser Dutchmen or Renaissance. It's about teen culture after all.\n\n "
            "It's important to notice, that the author was initially so confused by these genres, that actually "
            "incorrectly attributed Breakcore to one of them. In deeply theoretical meaning (according to aesthetics "
            "wiki), this is just a music genre, however in practice one can probably find some distinguishable "
            "visual features of it. \n\nWhat this all means to you is that Breakcore pictures are often missclassified. "
            "What this means to humanity is that we are shaping the visual representation of this genre here and now, "
            "since that's new cultural trends emerge after all!")

    async def start_conversation(event):
        await break_chat_context(event)
        sender_id = event.sender_id
        if conversation_state.get(sender_id, None) is not None:
            await break_chat_context(event)
        else:
            await event.respond(
                "Welcome to the Corephaeus! \n\nIf you feel yourself lost in a fast-paced world of teenage culture "
                "but don't want to lose your face among the youngsters when speaking about things like Glitchcore or "
                "Weirdcore, this bot is for you. \n\n"
                "Type /which and send me a picture to determine the aesthetic genre and seem cool and intellignet "
                "among the 15yr-olds!")
            conversation_state[sender_id] = ChatState.EXISTING_CONV

    async def which_core_context(event):
        await break_chat_context(event)
        sender_id = event.sender_id
        async with client.conversation(sender_id, exclusive=False) as conv:
            await conv.send_message('Let me look at the image')
            try:
                while True:
                    resp_msg = await conv.get_response()
                    if resp_msg.photo is not None:
                        await conv.send_message(random.choice([
                            'Uuuh', 'Let me think', 'Cool one!', 'Whoah', 'I think I know the answer']))
                        img_file_name = f'{IMAGE_SAVE_PATH}/{uuid.uuid4().hex}.jpg'
                        await resp_msg.download_media(img_file_name)
                        await conv.send_message(model(img_file_name))
                        if not save_images:
                            if os.path.exists(img_file_name):
                                os.remove(img_file_name)
                            else:
                                logging.warning("Attempted to delete non-existent file")
                        return
                    else:
                        await conv.send_message('Send an image or type /cancel')
            except asyncio.exceptions.TimeoutError:
                await conv.send_message("Session expired")
                await break_chat_context(event)

    @client.on(events.NewMessage(pattern=r'/.*'))
    async def event_handler(event):
        match event.raw_text:
            case '/start':
                await start_conversation(event)
            case '/about':
                await about_context(event)
            case '/which':
                await which_core_context(event)
            case '/cancel':
                await break_chat_context(event)

    await client.run_until_disconnected()
