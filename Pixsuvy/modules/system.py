import sys
from os import environ, execle

from pyrogram import Client, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from Pixsuvy import BOTLOG_CHATID, LOGGER
from Pixsuvy.helpers.basic import edit_or_reply
from Pixsuvy.helpers.misc import HAPP

from .help import add_command_help


@Client.on_message(filters.command("restart", cmd) & filters.me)
async def restart_bot(_, message: Message):
    try:
        msg = await edit_or_reply(message, "`Restarting bot...`")
        LOGGER(__name__).info("BOT SERVER RESTARTED !!")
    except BaseException as err:
        LOGGER(__name__).info(f"{err}")
        return
    await msg.edit_text("Pixsuvy has restarted !\n\n")
    if HAPP is not None:
        HAPP.restart()
    else:
        args = [sys.executable, "-m", "Pixsuvy"]
        execle(sys.executable, *args, environ)


@Client.on_message(filters.command("shutdown", cmd) & filters.me)
async def shutdown_bot(client: Client, message: Message):
    if BOTLOG_CHATID:
        await client.send_message(
            BOTLOG_CHATID,
            "**#SHUTDOWN** \n"
            "**Pixsuvy** has been turned off",
        )
    await edit_or_reply(message, "**Pixsuvy Successfully shut down!**")
    if HAPP is not None:
        HAPP.process_formation()["worker"].scale(0)
    else:
        sys.exit(0)


add_command_help(
    "system",
    [
        ["restart", "To restart the userbot."],
        ["shutdown", "To shut down the userbot."],
    ],
)
