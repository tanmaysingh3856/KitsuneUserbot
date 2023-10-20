import requests
from pyrogram import filters, Client
from pyrogram.types import Message
from .help import add_command_help
from config import CMD_HANDLER as cmd

API = "https://api.nekosapi.com/v2/images/random"

@Client.on_message(filters.command("anime", cmd) & filters.me)
async def anime(client: Client, message: Message):
    await message.edit("Fetching a random anime image...")
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()["data"]["attributes"]
        image_url = data["file"]
        title = data["title"]
    except (requests.exceptions.RequestException, KeyError):
        await message.edit("Failed to fetch a random anime image.")
        return
    await client.send_photo(message.chat.id, image_url, caption=f"**Title:** {title}")
    await message.edit("Random anime image sent!")

add_command_help(
    "anime",
    [
        ["anime <anime name>", "Get information about a anime."],
    ],
)