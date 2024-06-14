import asyncio
import os
import time
from platform import python_version

from pyrogram import Client
from pyrogram import __version__ as versipyro
from pyrogram import filters
from pyrogram.types import Message
from telegraph import exceptions, upload_file

from config import BOT_VER
from config import CMD_HANDLER as cmd
from Kitsune import CMD_HELP, StartTime
from Kitsune.helpers.basic import edit_or_reply
from Kitsune.helpers.PyroHelpers import ReplyCheck
from Kitsune.helpers.SQL.globals import gvarstatus
from Kitsune.helpers.tools import convert_to_image
from Kitsune.utils import get_readable_time
from Kitsune.utils.misc import restart

from .help import add_command_help

modules = CMD_HELP
alive_logo = (
    gvarstatus("ALIVE_LOGO") or "https://graph.org/file/9a184d8c18fd04134c8a1.png"
)
emoji = gvarstatus("ALIVE_EMOJI") or "⚡️"
alive_text = gvarstatus("ALIVE_TEKS_CUSTOM") or "Hey, I am alive."


@Client.on_message(filters.command(["alive", "awake"], cmd) & filters.me)
async def alive(client: Client, message: Message):
    xx = await edit_or_reply(message, "⚡️")
    await asyncio.sleep(2)
    send = client.send_video if alive_logo.endswith(".mp4") else client.send_photo
    uptime = await get_readable_time((time.time() - StartTime))
    pix = (
        f"**Kitsune is Up and Running.**\n\n"
        f"<b>{alive_text}</b>\n\n"
        f"{emoji} <b>Master :</b> {client.me.mention} \n"
        f"{emoji} <b>Modules :</b> <code>{len(modules)} Modules</code> \n"
        f"{emoji} <b>Bot Version :</b> <code>{BOT_VER}</code> \n"
        f"{emoji} <b>Python Version :</b> <code>{python_version()}</code> \n"
        f"{emoji} <b>Pyrogram Version :</b> <code>{versipyro}</code> \n"
        f"{emoji} <b>Bot Uptime :</b> <code>{uptime}</code> \n\n"
    )
    try:
        await asyncio.gather(
            xx.delete(),
            send(
                message.chat.id,
                alive_logo,
                caption=pix,
                reply_to_message_id=ReplyCheck(message),
            ),
        )
    except BaseException:
        await xx.edit(pix, disable_web_page_preview=True)


@Client.on_message(filters.command("setalivelogo", cmd) & filters.me)
async def setalivelogo(client: Client, message: Message):
    try:
        import Kitsune.helpers.SQL.globals as sql
    except AttributeError:
        await message.edit("**Running on Non-SQL mode!**")
        return
    pix = await edit_or_reply(message, "`Processing...`")
    link = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message.media:
        if message.reply_to_message.sticker:
            m_d = await convert_to_image(message, client)
        else:
            m_d = await message.reply_to_message.download()
        try:
            media_url = upload_file(m_d)
        except exceptions.TelegraphException as exc:
            await pix.edit(f"**ERROR:** `{exc}`")
            os.remove(m_d)
            return
        link = f"https://telegra.ph/{media_url[0]}"
        os.remove(m_d)
    sql.addgvar("ALIVE_LOGO", link)
    await pix.edit(
        f"**Successfully changed ALIVE logo = {link}**",
        disable_web_page_preview=True,
    )
    restart()


@Client.on_message(filters.command("setalivetext", cmd) & filters.me)
async def setalivetext(client: Client, message: Message):
    try:
        import Kitsune.helpers.SQL.globals as sql
    except AttributeError:
        await message.edit("**Running on Non-SQL mode!**")
        return
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    pix = await edit_or_reply(message, "`Processing...`")
    if not text:
        return await edit_or_reply(message, "**Give a Text or Reply to text**")
    sql.addgvar("ALIVE_TEKS_CUSTOM", text)
    await pix.edit(f"**Successfully Customizing ALIVE TEXT ** `{text}`")
    restart()


@Client.on_message(filters.command("setemoji", cmd) & filters.me)
async def setemoji(client: Client, message: Message):
    try:
        import Kitsune.helpers.SQL.globals as sql
    except AttributeError:
        await message.edit("**Running on Non-SQL mode!**")
        return
    emoji = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    pix = await edit_or_reply(message, "`Processing...`")
    if not emoji:
        return await edit_or_reply(message, "**Give An Emoji**")
    sql.addgvar("ALIVE_EMOJI", emoji)
    await pix.edit(f"**Successfully Custom EMOJI ALIVE is** {emoji}")
    restart()


add_command_help(
    "alive",
    [
        [
            "alive",
            "To check your userbot is working or not",
        ],
        [
            "setalivelogo <link telegraph or reply to photo/video/gif>",
            "To customize your userbot alive logo",
        ],
        [
            "setalivetext <text>",
            "To customize your userbot's alive text",
        ],
        [
            "setemoji <emoji>",
            "To customize your emoji alive userbot",
        ],
    ],
)
