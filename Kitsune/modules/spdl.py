import asyncio

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from Kitsune import *
from Kitsune.helpers.PyroHelpers import ReplyCheck
from Kitsune.helpers.tools import get_arg

from .help import *


@Client.on_message(filters.command(["spdl"], cmd) & filters.me)
async def sosmed(client: Client, message: Message):
    Pix = await message.edit("`Processing . . .`")
    link = get_arg(message)
    bot = "CatMusicRobot"
    if link:
        try:
            xd = await client.send_message(bot, link)
            await asyncio.sleep(5)
            await xd.delete()
        except YouBlockedUser:
            await client.unblock_user(bot)
            xd = await client.send_message(bot, link)
            await asyncio.sleep(5)
            await xd.delete()
    async for sosmed in client.search_messages(
        bot, filter=enums.MessagesFilter.AUDIO, limit=1
    ):
        await asyncio.gather(
            Pix.delete(),
            client.send_audio(
                message.chat.id,
                sosmed.audio.file_id,
                caption=f"**Uploaded by:** {client.me.mention}",
                reply_to_message_id=ReplyCheck(message),
            ),
        )
        await client.delete_messages(bot, 2)


add_command_help(
    "spdl",
    [
        [
            f"spdl <link>",
            "download songs from Spotify",
        ],
    ],
)
