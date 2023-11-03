from googlesearch import search
from pyrogram import Client, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from Pixsuvy.helpers.basic import edit_or_reply

from .help import *


def gsearch(query):
    co = 1
    returnquery = {}
    for j in search(query, sleep_interval=10, advanced=True):
        site_title = j.title
        metadeta = j.description
        j.url
        returnquery[co] = {"title": site_title, "metadata": metadeta, "url": j}
        co = co + 1
    return returnquery


@Client.on_message(filters.command(["gs", "google"], cmd) & filters.me)
async def gs(client: Client, message: Message):
    slr = await edit_or_reply(message, "`Processing...`")
    returnmsg = ""
    query = None
    try:
        query = message.text.split(" ", 1)[1]
    except:
        return await slr.edit("Give a query to search")
    results = gsearch(query)
    for i in range(1, 10, 1):
        presentquery = results[i]
        presenttitle = presentquery["title"]
        presentmeta = presentquery["metadata"]
        presenturl = presentquery["url"]
        print(presentquery)
        print(presenttitle)
        print(presentmeta)
        print(presenturl)
        if not presentmeta:
            presentmeta = ""
        else:
            presentmeta = presentmeta[0]
        returnmsg = (
            returnmsg
            + f"[{str(presenttitle)}]({str(presenturl)})\n{str(presentmeta)}\n\n"
        )
    await slr.edit(returnmsg)


add_command_help(
    "google",
    [
        [
            "google",
            "Fetch Details on Google.",
        ],
    ],
)
