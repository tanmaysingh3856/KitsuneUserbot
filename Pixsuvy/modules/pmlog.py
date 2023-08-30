import asyncio

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from config import PMLOG_CHATID
from Pixsuvy.helpers.basic import edit_or_reply
from Pixsuvy.helpers.SQL import no_log_pms_sql
from Pixsuvy.helpers.SQL.globals import addgvar, gvarstatus
from Pixsuvy.helpers.tools import get_arg

from .help import add_command_help


class LOG_CHATS:
    def __init__(self):
        self.RECENT_USER = None
        self.NEWPM = None
        self.COUNT = 0


LOG_CHATS_ = LOG_CHATS()


@Client.on_message(
    filters.private & filters.incoming & ~filters.service & ~filters.me & ~filters.bot
)
async def monito_p_m_s(client: Client, message: Message):
    if PMLOG_CHATID == -100:
        return
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        return
    if not no_log_pms_sql.is_approved(message.chat.id) and message.chat.id != 777000:
        if LOG_CHATS_.RECENT_USER != message.chat.id:
            LOG_CHATS_.RECENT_USER = message.chat.id
            if LOG_CHATS_.NEWPM:
                await LOG_CHATS_.NEWPM.edit(
                    LOG_CHATS_.NEWPM.text.replace(
                        "** #NEW_MESSAGE**",
                        f" • `{LOG_CHATS_.COUNT}` **Message**",
                    )
                )
                LOG_CHATS_.COUNT = 0
            LOG_CHATS_.NEWPM = await client.send_message(
                PMLOG_CHATID,
                f" <b>#CONTINUE #NEW_MESSAGE</b>\n<b> • From :</b> {message.from_user.mention}\n<b> • User ID :</b> <code>{message.from_user.id}</code>",
                parse_mode=enums.ParseMode.HTML,
            )
        try:
            async for pmlog in client.search_messages(message.chat.id, limit=1):
                await pmlog.forward(PMLOG_CHATID)
            LOG_CHATS_.COUNT += 1
        except BaseException:
            pass


@Client.on_message(filters.group & filters.mentioned & filters.incoming)
async def log_tagged_messages(client: Client, message: Message):
    if PMLOG_CHATID == -100:
        return
    if gvarstatus("GRUPLOG") and gvarstatus("GRUPLOG") == "false":
        return
    if (no_log_pms_sql.is_approved(message.chat.id)) or (PMLOG_CHATID == -100):
        return
    result = f"<b> #TAGS #MESSAGE</b>\n<b> • From : </b>{message.from_user.mention}"
    result += f"\n<b> • group : </b>{message.chat.title}"
    result += f"\n<b> • Message link </b><a href = '{message.link}'>View </a>"
    result += f"\n<b> • Message : </b><code>{message.text}</code>"
    await asyncio.sleep(0.5)
    await client.send_message(
        PMLOG_CHATID,
        result,
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )


@Client.on_message(filters.command("log", cmd) & filters.me)
async def set_log_p_m(client: Client, message: Message):
    if PMLOG_CHATID != -100:
        if no_log_pms_sql.is_approved(message.chat.id):
            no_log_pms_sql.disapprove(message.chat.id)
            await message.edit("**LOG Chat from this Group Activated Successfully**")


@Client.on_message(filters.command("nolog", cmd) & filters.me)
async def set_no_log_p_m(client: Client, message: Message):
    if PMLOG_CHATID != -100:
        if not no_log_pms_sql.is_approved(message.chat.id):
            no_log_pms_sql.approve(message.chat.id)
            await message.edit("**LOG Chat from this Group Deactivated Successfully**")


@Client.on_message(filters.command(["pmlog", "pmlogger"], cmd) & filters.me)
async def set_pmlog(client: Client, message: Message):
    if PMLOG_CHATID == -100:
        return await message.edit(
            "**To Use this Module, you Must Set Up** `PMLOG_CHATID` **in Config var**"
        )
    input_str = get_arg(message)
    if input_str == "off":
        h_type = False
    elif input_str == "on":
        h_type = True
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        PMLOG = False
    else:
        PMLOG = True
    if PMLOG:
        if h_type:
            await edit_or_reply(message, "**PM LOG Already Activated**")
        else:
            addgvar("PMLOG", h_type)
            await edit_or_reply(message, "**PM LOG Deactivated Successfully**")
    elif h_type:
        addgvar("PMLOG", h_type)
        await edit_or_reply(message, "**PM LOG Activated Successfully**")
    else:
        await edit_or_reply(message, "**PM LOG Has Been Turned Off**")


@Client.on_message(filters.command(["gruplog", "grouplog", "gclog"], cmd) & filters.me)
async def set_gruplog(client: Client, message: Message):
    if PMLOG_CHATID == -100:
        return await message.edit(
            "**To Use this Module, you Must Set Up** `PMLOG_CHATID` **in Config Vars**"
        )
    input_str = get_arg(message)
    if input_str == "off":
        h_type = False
    elif input_str == "on":
        h_type = True
    if gvarstatus("GRUPLOG") and gvarstatus("GRUPLOG") == "false":
        GRUPLOG = False
    else:
        GRUPLOG = True
    if GRUPLOG:
        if h_type:
            await edit_or_reply(message, "**Group Log Already Enabled**")
        else:
            addgvar("GRUPLOG", h_type)
            await edit_or_reply(message, "**Group Log Deactivated Successfully**")
    elif h_type:
        addgvar("GRUPLOG", h_type)
        await edit_or_reply(message, "**Group Log Activated Successfully**")
    else:
        await edit_or_reply(message, "**Group Logs Has Been Turned Off**")


add_command_help(
    "pmlog",
    [
        [
            "log",
            "To enable Chat Log of that chat/group.",
        ],
        [
            "nolog",
            "To disable Chat Logs from that chat/group.",
        ],
        [
            "pmlog on/off",
            "To enable or disable private log messages to be forwarded to the log group.",
        ],
        [
            "gruplog on/off",
            "To activate or deactivate the group tag, which will go to the log group.",
        ],
    ],
)
