import logging
import asyncio
import os

from os import environ
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

logging.basicConfig(level=logging.ERROR)

channels_str = os.environ.get("CHANNELS")
if channels_str is not None:
    CHANNELS = [int(CHANNEL) for CHANNEL in channels_str.split()]
else:
    # Handle the case when CHANNELS is not provided
    CHANNELS = []

AuthChat = filters.chat(CHANNELS) if CHANNELS else (filters.group | filters.channel)         
User = Client(
    "AcceptUser",
    api_id=int(environ.get("API_ID")),
    api_hash=environ.get("API_HASH"),
    session_string=environ.get("SESSION")
)


@User.on_message(filters.command(["run", "approve", "start"], [".", "/"]) & AuthChat)                     
async def approve(client: User, message: Message):
    Id = message.chat.id
    await message.delete(True)

    try:
        while True:
            try:
                await client.approve_all_chat_join_requests(Id)
            except FloodWait as t:
                await asyncio.sleep(t.x)  # Sleep for the specified flood wait time
                await client.approve_all_chat_join_requests(Id)
            except Exception as e:
                logging.error(str(e))
    except FloodWait as s:
        await asyncio.sleep(s.x)  # Sleep for the specified flood wait time
        while True:
            try:
                await client.approve_all_chat_join_requests(Id)
            except FloodWait as t:
                await asyncio.sleep(t.x)  # Sleep for the specified flood wait time
                await client.approve_all_chat_join_requests(Id)
            except Exception as e:
                logging.error(str(e))

    msg = await client.send_message(Id, "**Task Completed** ✓ **Approved Pending All Join Request**")
    await asyncio.sleep(3)
    await msg.delete()


logging.info("Bot Started....")
User.run()

