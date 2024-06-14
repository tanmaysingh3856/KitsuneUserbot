from pyrogram import Client, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from Kitsune import *
from Kitsune.helpers.basic import edit_or_reply

from .help import *


@Client.on_message(filters.command(["ss"], cmd) & filters.me)
async def webshot(client: Client, message: Message):
    pix = await edit_or_reply(message, "`Processing...`")
    try:
        user_link = message.command[1]
        try:
            full_link = f"https://webshot.deam.io/{user_link}/?width=1920&height=1080?delay=2000?type=png"
            await client.send_photo(
                message.chat.id,
                full_link,
                caption=f"**Screenshot of the page ⟶** {user_link}",
            )
        except Exception as dontload:
            await message.edit(f"Error! {dontload}\nTrying again create screenshot...")
            full_link = f"https://mini.s-shot.ru/1920x1080/JPEG/1024/Z100/?{user_link}"
            await client.send_photo(
                message.chat.id,
                full_link,
                caption=f"**Screenshot of the page ⟶** {user_link}",
            )
        await pix.delete()
    except Exception as error:
        await pix.delete()
        await client.send_message(
            message.chat.id, f"**Something went wrong\nLog:{error}...**"
        )


add_command_help(
    "webshot",
    [
        [
            f"ss <link>",
            "To screenshot a given web page .",
        ],
    ],
)
