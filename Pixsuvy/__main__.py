import importlib

from pyrogram import idle
from uvloop import install

from config import BOT_VER, CMD_HANDLER
from Pixsuvy import BOTLOG_CHATID, LOGGER, LOOP, aiosession, bot1, bots
from Pixsuvy.helpers.misc import create_botlog, heroku
from Pixsuvy.modules import ALL_MODULES

PIX_ON = "Pixsuvy Userbot has been started"


async def main():
    for all_module in ALL_MODULES:
        importlib.import_module(f"Pixsuvy.modules.{all_module}")
    for bot in bots:
        try:
            await bot.start()
            bot.me = await bot.get_me()
            try:
                await bot.send_message(
                    BOTLOG_CHATID, PIX_ON.format(BOT_VER, CMD_HANDLER)
                )
            except BaseException:
                pass
            LOGGER("Pixsuvy").info(
                f"Logged in as {bot.me.first_name} | [ {bot.me.id} ]"
            )
        except Exception as a:
            LOGGER("main").warning(a)
    LOGGER("Pixsuvy").info(f"Pixsuvy v{BOT_VER}")
    if bot1 and not str(BOTLOG_CHATID).startswith("-100"):
        await create_botlog(bot1)
    await idle()
    await aiosession.close()


if __name__ == "__main__":
    LOGGER("Pixsuvy").info("Starting Pixsuvy")
    install()
    heroku()
    LOOP.run_until_complete(main())
