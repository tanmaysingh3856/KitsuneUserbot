import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from Pixsuvy import bot1
from Pixsuvy.helpers.PyroHelpers import ReplyCheck

from .help import add_command_help


@Client.on_message(filters.command("dmusic", cmd) & filters.me)
async def send_music(bot: Client, message: Message):
    try:
        cmd = message.command

        song_name = ""
        if len(cmd) > 1:
            song_name = " ".join(cmd[1:])
        elif message.reply_to_message and len(cmd) == 1:
            song_name = (
                message.reply_to_message.text or message.reply_to_message.caption
            )
        elif not message.reply_to_message and len(cmd) == 1:
            await message.edit("Give a song name")
            await asyncio.sleep(2)
            await message.delete()
            return

        song_results = await bot1.get_inline_bot_results("deezermusicbot", song_name)

        try:
            # send to Saved Messages because hide_via doesn't work sometimes
            saved = await bot.send_inline_bot_result(
                chat_id="me",
                query_id=song_results.query_id,
                result_id=song_results.results[0].id,
                hide_via=True,
            )

            # forward as a new message from Saved Messages
            saved = await Client.get_messages("me", int(saved.updates[1].message.id))
            message.reply_to_message.id if message.reply_to_message else None
            await bot.send_audio(
                chat_id=message.chat.id,
                audio=str(saved.audio.file_id),
                reply_to_message_id=ReplyCheck(message),
            )

            # delete the message from Saved Messages
            await Client.delete_messages("me", saved.id)
        except TimeoutError:
            await message.edit("That didn't work out")
            await asyncio.sleep(2)
        await message.delete()
    except Exception as e:
        print(e)
        await message.edit("`Failed to find song`")
        await asyncio.sleep(2)
        await message.delete()


# Command help section
add_command_help("deezer", [["dmusic", "Search songs and send, Deezer bot"]])
