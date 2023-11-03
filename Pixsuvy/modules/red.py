import pyrogram.enums
from pyrogram import Client, filters
from pyrogram.types import Message

from .help import add_command_help


# Generate full Reddit link with subreddit
@Client.on_message(filters.regex("^r\/([^\s\/])+") & filters.me)
async def subreddit_link(bot: Client, message: Message):
    html = "<a href='{link}'>{string}</a>"
    await message.edit(
        html.format(link="https://reddit.com/" + message.text, string=message.text),
        disable_web_page_preview=True,
        parse_mode=pyrogram.enums.ParseMode.HTML,
    )


# Command help section
add_command_help(
    "redlinks",
    [
        [
            "r/telegram",
            "As long as your message starts with r/, it will automatically generate a subreddit link and "
            "hyperlink your message.",
        ],
    ],
)
