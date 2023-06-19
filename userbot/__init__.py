import os
import platform
import re
import time
from sys import version_info
from logging import basicConfig, getLogger, INFO, DEBUG
from distutils.util import strtobool as sb
from .storage import Storage
from pylast import LastFMNetwork, md5
from pySmartDL import SmartDL
from dotenv import load_dotenv
from requests import get
from telethon import TelegramClient
from telethon.sessions import StringSession
from git import Repo
from platform import python_version, uname
from telethon import __version__, version

load_dotenv("config.env")

STORAGE = (lambda n: Storage(Path("data") / n))

StartTime = time.time()
HELP_TIMEOUT = sb(os.environ.get("HELP_TIMEOUT") or "False")
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get(
    "CONSOLE_LOGGER_VERBOSE") or "False")

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=INFO)
LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 8:
    LOGS.info(
        "You MUST have a python version of at least 3.8."
        "Multiple features depend on this. Bot quitting."
    )
    quit(1)

repo_link = Repo().remotes.origin.url.split('.git')[0].split('.com/')[1] if Repo().remotes.origin.url else "null"
LOGS.info(f"Starting Pixsuvy  Userbot on {repo_link}")

CONFIG_CHECK = (os.environ.get(
    "___________PLOX_______REMOVE_____THIS_____LINE__________") or None)

if CONFIG_CHECK:
    LOGS.info(
        "Please remove the line mentioned in the first hashtag from the config.env file"
    )
    quit(1)
CMD_LIST={}
# Telegram App KEY and HASH
API_KEY = os.environ.get("API_KEY") or None
API_HASH = os.environ.get("API_HASH") or None
SUDO_USERS = {int(x) for x in os.environ.get("SUDO_USERS", "").split()}
DEVS = 2031166458

STRING_SESSION = os.environ.get("STRING_SESSION") or None

DEEZER_ARL_TOKEN = os.environ.get("DEEZER_ARL_TOKEN") or None

BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID") or 0)

BOTLOG = sb(os.environ.get("BOTLOG") or "False")
if BOTLOG:
    LOGSP = sb(os.environ.get("LOGSP") or "False")
else:
    LOGSP = False

CMD_HANDLER = os.environ.get("CMD_HANDLER", r".")
LOG_TAGGING = sb(os.environ.get("LOG_TAGGING") or "False")
LOG_TAGGING_CHATID = int(os.environ.get("LOG_TAGGING_CHATID") or 0)

PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN") or "False")

HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME") or None
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY") or None
GIT_REPO_NAME = os.environ.get("GIT_REPO_NAME") or None
GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN") or None

# Custom (forked) repo URL and BRANCH for updater.
UPSTREAM_REPO_URL = (os.environ.get("UPSTREAM_REPO_URL")
                     or "https://github.com/Pixsuvy/Pixsuvyuserbot.git")
UPSTREAM_REPO_BRANCH = os.environ.get("UPSTREAM_REPO_BRANCH") or "main"

CONSOLE_LOGGER_VERBOSE = sb(os.environ.get(
    "CONSOLE_LOGGER_VERBOSE") or "False")

DB_URI = os.environ.get("DATABASE_URL") or None

OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY") or None

REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY") or None

CHROME_DRIVER = "/usr/bin/chromedriver"
GOOGLE_CHROME_BIN = "/usr/bin/chromium-browser"

OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID") or None
WEATHER_DEFCITY = os.environ.get("WEATHER_DEFCITY") or None
WEATHER_DEFLANG = os.environ.get("WEATHER_DEFLANG") or None

GENIUS = os.environ.get("GENIUS_ACCESS_TOKEN") or None

WOLFRAM_ID = os.environ.get("WOLFRAM_ID") or None

# Anti Spambot Config
ANTI_SPAMBOT = sb(os.environ.get("ANTI_SPAMBOT") or "False")
ANTI_SPAMBOT_SHOUT = sb(os.environ.get("ANTI_SPAMBOT_SHOUT") or "False")

ALIVE_NAME = os.environ.get("ALIVE_NAME") or None

ALIVE_LOGO = str(os.environ.get("ALIVE_LOGO") or "https://github.com/pixsuvy/resources/blob/main/Pixlogo.jpg")
ALIVE_MESSAGE = str(os.environ.get("ALIVE_MESSAGE") or "")

TIMEOUT = sb(os.environ.get("TIMEOUT") or "True")
COUNTRY = str(os.environ.get("COUNTRY") or "")
TZ_NUMBER = os.environ.get("TZ_NUMBER") or 1

USERBOT_VERSION = "0.1"

USER_TERM_ALIAS = os.environ.get("USER_TERM_ALIAS") or "pixsuvy"

UPDATER_ALIAS = os.environ.get("UPDATER_ALIAS") or "Pixsuvy Userbot"

ZIP_DOWNLOAD_DIRECTORY = os.environ.get("ZIP_DOWNLOAD_DIRECTORY") or "./zips"

CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME") or "True")

BIO_PREFIX = os.environ.get("BIO_PREFIX") or None
DEFAULT_BIO = os.environ.get("DEFAULT_BIO") or None

LASTFM_API = os.environ.get("LASTFM_API") or None
LASTFM_SECRET = os.environ.get("LASTFM_SECRET") or None
LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME") or None
LASTFM_PASSWORD_PLAIN = os.environ.get("LASTFM_PASSWORD") or None
LASTFM_PASS = md5(LASTFM_PASSWORD_PLAIN)
if LASTFM_API is not None:
    lastfm = LastFMNetwork(
        api_key=LASTFM_API,
        api_secret=LASTFM_SECRET,
        username=LASTFM_USERNAME,
        password_hash=LASTFM_PASS,
    )
else:
    lastfm = None

G_DRIVE_DATA = os.environ.get("G_DRIVE_DATA") or None
G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID") or None
G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET") or None
G_DRIVE_AUTH_TOKEN_DATA = os.environ.get("G_DRIVE_AUTH_TOKEN_DATA") or None
G_DRIVE_FOLDER_ID = os.environ.get("G_DRIVE_FOLDER_ID") or None
GDRIVE_INDEX_URL = os.environ.get("GDRIVE_INDEX_URL") or None
TEMP_DOWNLOAD_DIRECTORY = os.environ.get(
    "TMP_DOWNLOAD_DIRECTORY") or "./downloads/"

USR_TOKEN = os.environ.get("USR_TOKEN_UPTOBOX", None)
SFUSER = os.environ.get("SFUSER") or "null"
SFPASS = os.environ.get("SFPASS") or "null"
SFDIR = os.environ.get("SFDIR") or "null"

MEGA_EMAIL = os.environ.get("MEGA_EMAIL") or None
MEGA_PASSWORD = os.environ.get("MEGA_PASSWORD") or None

if not os.path.exists("bin"):
    os.mkdir("bin")

binaries = {
    "https://raw.githubusercontent.com/adekmaulana/megadown/master/megadown": "bin/megadown",
    "https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py": "bin/cmrudl",
}

for binary, path in binaries.items():
    downloader = SmartDL(binary, path, progress_bar=False)
    downloader.start()
    os.chmod(path, 0o755)
'
if STRING_SESSION:
    bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    bot = TelegramClient("userbot", API_KEY, API_HASH)


async def check_botlog_chatid():
    if not BOTLOG:
        return

    entity = await bot.get_entity(BOTLOG_CHATID)
    if entity.default_banned_rights.send_messages:
        LOGS.info(
            "Your account doesn't have rights to send messages to BOTLOG_CHATID "
            "group. Check if you typed the Chat ID correctly.")
        quit(1)


with bot:
    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except BaseException:
        LOGS.info(
            "BOTLOG_CHATID environment variable isn't a "
            "valid entity. Check your environment variables/config.env file."
        )
        quit(1)
        
async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time

COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
CMD_HELP = {}
ZALG_LIST = {}
ISAFK = False
AFKREASON = None
DELMSG = False

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
repo = Repo()
modules = CMD_HELP
uptime = time.strftime('%X')
