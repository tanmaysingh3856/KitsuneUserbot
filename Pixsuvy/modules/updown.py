import asyncio
import math
import os
import time
from datetime import datetime

import humanize
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageIdInvalid, MessageNotModified
from pyrogram.types import Message
from pySmartDL import SmartDL

from config import CMD_HANDLER as cmd
from Pixsuvy.helpers.basic import edit_or_reply

from .help import add_command_help


async def progress_for_pyrogram(current, total, ud_type, message, start):
    """generic progress display for Telegram Upload / Download status"""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        elapsed_time = round(diff)
        if elapsed_time == 0:
            return
        speed = current / diff
        time_to_completion = round((total - current) / speed)
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = time_formatter(elapsed_time)
        estimated_total_time = time_formatter(estimated_total_time)

        progress = "[{0}{1}] \nP: {2}%\n".format(
            "".join(["▰" for _ in range(math.floor(percentage / 5))]),
            "".join(["▱" for _ in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2),
        )

        tmp = progress + "{0} of {1}\nSpeed: {2}/s\nETA: {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != "" else "0 s",
        )
        try:
            await message.edit(f"{ud_type}\n {tmp}")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.edit(f"{ud_type}\n {tmp}")
        except (MessageNotModified, MessageIdInvalid):
            pass


def humanbytes(size: int) -> str:
    """converts bytes into human readable format"""
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    number = 0
    dict_power_n = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        number += 1
    return f"{str(round(size, 2))} {dict_power_n[number]}B"


def time_formatter(seconds: int) -> str:
    result = ""
    v_m = 0
    remainder = seconds
    r_ange_s = {"days": (24 * 60 * 60), "hours": (60 * 60), "minutes": 60, "seconds": 1}
    for age, divisor in r_ange_s.items():
        v_m, remainder = divmod(remainder, divisor)
        v_m = int(v_m)
        if v_m != 0:
            result += f" {v_m} {age} "
    return result


async def progress_callback(current, total, bot: Client, message: Message):
    if int((current / total) * 100) % 25 == 0:
        await message.edit(
            f"{humanize.naturalsize(current)} / {humanize.naturalsize(total)}"
        )


@Client.on_message(filters.command(["download"], cmd) & filters.me)
async def download(client, message):
    xyz = await edit_or_reply(message, "`proccessing . . .`")
    if message.reply_to_message is not None:
        start_t = datetime.now()
        c_time = time.time()
        the_real_download_location = await client.download_media(
            message=message.reply_to_message,
            progress=progress_for_pyrogram,
            progress_args=("trying to download, please be patient..", xyz, c_time),
        )
        end_t = datetime.now()
        ms = (end_t - start_t).seconds
        await xyz.edit(
            f"Downloaded to <code>{the_real_download_location}</code> in <u>{ms}</u> seconds."
        )
    elif len(message.command) > 1:
        start_t = datetime.now()
        the_url_parts = " ".join(message.command[1:])
        url = the_url_parts.strip()
        custom_file_name = os.path.basename(url)
        if "|" in the_url_parts:
            url, custom_file_name = the_url_parts.split("|")
            url = url.strip()
            custom_file_name = custom_file_name.strip()
        download_file_path = os.path.join("downloads/", custom_file_name)
        downloader = SmartDL(url, download_file_path, progress_bar=False)
        downloader.start(blocking=False)
        c_time = time.time()
        while not downloader.isFinished():
            total_length = downloader.filesize or None
            downloaded = downloader.get_dl_size(human=True)
            display_message = ""
            now = time.time()
            diff = now - c_time
            percentage = downloader.get_progress() * 100
            speed = downloader.get_speed(human=True)
            round(diff) * 1000
            progress_str = "[{0}{1}]\nProgress: {2}%".format(
                "".join(["█" for _ in range(math.floor(percentage / 5))]),
                "".join(["░" for _ in range(20 - math.floor(percentage / 5))]),
                round(percentage, 2),
            )

            estimated_total_time = downloader.get_eta(human=True)
            try:
                current_message = "Trying to download...\n"
                current_message += f"URL: <code>{url}</code>\n"
                current_message += f"File Name: <code>{custom_file_name}</code>\n"
                current_message += f"Speed: {speed}\n"
                current_message += f"{progress_str}\n"
                current_message += (
                    f"{humanbytes(downloaded)} of {humanbytes(total_length)}\n"
                )
                current_message += f"ETA: {estimated_total_time}"
                if round(diff % 10.00) == 0 and current_message != display_message:
                    await xyz.edit(disable_web_page_preview=True, text=current_message)
                    display_message = current_message
                    await asyncio.sleep(10)
            except Exception as e:
                LOGGER.info(str(e))
        if os.path.exists(download_file_path):
            end_t = datetime.now()
            ms = (end_t - start_t).seconds
            await xyz.edit(
                f"Downloaded to <code>{download_file_path}</code> in {ms} seconds"
            )
    else:
        await xyz.edit("Reply to a Telegram Media, to download it to my local server.")


@Client.on_message(filters.command("upload", cmd) & filters.me)
async def upload_helper(bot: Client, message: Message):
    if len(message.command) > 1:
        await bot.send_document(
            message.chat.id,
            message.command[1],
            progress=progress_callback,
            progress_args=(bot, message),
        )
    else:
        await message.edit("No path provided.")
        await asyncio.sleep(3)

    await message.delete()


add_command_help(
    "upload",
    [
        [
            f"{cmd}upload",
            "Upload the file to telegram from the given system file path.",
        ],
    ],
)

add_command_help(
    "Download",
    [
        [
            f"{cmd}download",
            "Download the file to telegram.",
        ],
    ],
)
