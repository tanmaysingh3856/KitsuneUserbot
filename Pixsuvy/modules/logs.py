#by @who907
import requests
from pyrogram import Client, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from Pixsuvy.helpers.basic import edit_or_reply

from .help import add_command_help


@Client.on_message(filters.command("logs", cmd) & filters.me)
async def splogs(client: Client, message: Message):
    whew = await edit_or_reply(message, "`Getting logs . . .`")
    with open("logs.txt", "r") as f:
        lines = f.readlines()
    content = "".join(lines)
    link = spacebin(content)
    if link:
        await whew.edit_text(f"Pixsuvy logs: {link}", disable_web_page_preview=False)


def spacebin(content):
    payload = {"content": content, "extension": "none"}
    r = requests.post("https://spaceb.in/api/v1/documents/", data=payload).json()
    status = r["status"]
    if status == 201:
        did = r["payload"]["id"]
        link = f"https://spaceb.in/{did}"
        return link
    else:
        return None


add_command_help(
    "logs",
    [
        ["logs", "To view userbot logs."],
    ],
)
