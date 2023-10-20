import requests
from pyrogram import Client, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd

from .help import add_command_help

API = "https://api.nekosapi.com/v2/images/random"


@Client.on_message(filters.command("anime", cmd) & filters.me)
async def anime(client: Client, message: Message):
    if len(message.command) < 2:
        await message.edit("`Give me a anime name`")
        return
    query = message.text.split(None, 1)[1]
    try:
        r = requests.get(f"{API}?q={query}").json()
        anime = r["data"][0]
        title = anime["title"]
        description = anime["description"]
        image = anime["image"]
        await message.edit(
            f"**Title:** `{title}`\n\n**Description:** `{description}`",
            disable_web_page_preview=True,
        )
        await client.send_photo(
            message.chat.id,
            image,
            caption=f"**Title:** `{title}`\n\n**Description:** `{description}`",
        )
    except IndexError:
        await message.edit("`No anime found`")
        return
    except Exception as e:
        await message.edit(f"`{e}`")
        return


add_command_help(
    "anime",
    [
        ["anime <anime name>", "Get information about a anime."],
    ],
)
