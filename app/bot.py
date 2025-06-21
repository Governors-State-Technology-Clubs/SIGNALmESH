from pathlib import Path
from discord.ext import commands
from dotenv import load_dotenv

import discord
import logging
import os
import sys


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger: logging.Logger = logging.getLogger(__name__)


try:

    loaded: bool = load_dotenv(verbose=True)

    if not loaded:
        raise ValueError("No .env file was loaded")

    BOT_TOKEN = os.getenv("DISCORD_TOKEN")

    if BOT_TOKEN is None:
        raise TypeError("No BOT_TOKEN attribute in the .env file that loaded")

    CHANNEL_ID = os.getenv("GENERAL_CHANNEL_ID")

    if CHANNEL_ID is None:
        raise TypeError("No CHANNEL_ID attribute in the .env file that loaded")

except ValueError as ve:
    logger.exception(f"{ve}")
    sys.exit(1)

except TypeError as te:
    logger.exception(f"{te}")
    sys.exit(1)

root_dir: Path = Path.cwd()

intents: discord.Intents = discord.Intents.default()

intents.message_content = True

intents.members = True

bot: commands.Bot = commands.Bot(command_prefix="==", intents=intents)


@bot.event
async def on_ready():

    for server in bot.guilds:
        logger.info(f"Logged in as: {bot.user} on Server:{server.name} ID:{server.id}")

    logger.info(f"{bot.user} Ready")


bot.run(BOT_TOKEN, log_level=logging.DEBUG)
