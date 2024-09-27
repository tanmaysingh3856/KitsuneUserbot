import importlib
import tracemalloc
import asyncio
from pyrogram import idle
from uvloop import install
from config import BOT_VER, CMD_HANDLER
from Kitsune import BOTLOG_CHATID, LOGGER, LOOP, aiosession, bot1, bots
from Kitsune.helpers.misc import create_botlog, heroku
from Kitsune.modules import ALL_MODULES

PIX_ON = "Kitsune Userbot has been started"

# Enable tracemalloc
tracemalloc.start()


async def main():
    try:
        for all_module in ALL_MODULES:
            importlib.import_module(f"Kitsune.modules.{all_module}")
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
                LOGGER("Kitsune").info(
                    f"Logged in as {bot.me.first_name} | [ {bot.me.id} ]"
                )
            except Exception as a:
                LOGGER("main").warning(a)
        LOGGER("Kitsune").info(f"Kitsune v{BOT_VER}")
        if bot1 and not str(BOTLOG_CHATID).startswith("-100"):
            await create_botlog(bot1)
        await idle()
    except Exception as e:
        LOGGER("main").warning(f"Exception in main: {e}")
    finally:
        await aiosession.close()


if __name__ == "__main__":
    LOGGER("Kitsune").info("Starting Kitsune")
    install()
    heroku()
    LOOP.run_until_complete(main())
