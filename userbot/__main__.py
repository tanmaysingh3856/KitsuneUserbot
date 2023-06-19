from importlib import import_module
from sys import argv
from asyncio import sleep
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from userbot import LOGS, bot, HEROKU_APP_NAME, BOTLOG, BOTLOG_CHATID, ALIVE_NAME, USERBOT_VERSION, HEROKU_API_KEY, repo_link
from userbot.modules import ALL_MODULES
from telethon import __version__, version
from platform import python_version, uname

INVALID_PH = '\nERROR: The Phone No. entered is INVALID' \
             '\n Tip: Use Country Code along with number.' \
             '\n or check your phone number and try again !'

try:
    bot.start()
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info(f"You are running Pixsuvy Userbot on {repo_link}")

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
output = (
    "` =============================== `\n"
    f"`Pixsuvy UB is Up and Running.... `\n"
    f"`=============================== `\n"
    f"•`Telethon       : v{version.__version__} `\n"
    f"•`Python         : v{python_version()} `\n"
    f"•`User           : {DEFAULTUSER} `\n"
    f"•`Pixsuvy       : {USERBOT_VERSION} `\n"
)

async def start():
    if BOTLOG:
        try:
            await bot.send_message(
                BOTLOG_CHATID, output
                        )
        except:
            None
    else:
        pass
bot.loop.run_until_complete(start())

LOGS.info(
    "Congratulations, your userbot is now running !! Test it by typing .alive / .on in any chat."
    "If you need assistance, head to https://t.me/Pixsuvychat")
bot.run_until_disconnected()