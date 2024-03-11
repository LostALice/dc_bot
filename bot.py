# Code by Aki.no.Alice@Tyrant_Rex

import asyncio
import discord
import logging

from discord.ext import commands
from dotenv import load_dotenv
from os import getenv, listdir, environ

# logging
LOG_HANDLER = logging.FileHandler(
    filename="discord.log", encoding="utf-8", mode="w")

# load dev or release environment
load_dotenv(dotenv_path=".env")

if getenv("DEBUG") == "True":
    prefix = "-"
    logging_level = logging.INFO
else:
    logging_level = logging.ERROR
    prefix = getenv("PREFIX")
    if not prefix:
        prefix = "~"

client = commands.Bot(
    command_prefix=commands.when_mentioned_or(prefix),
    activity=discord.Game(
        name="OniiChan's Heart"
    ),
    intents=discord.Intents.all()
)

# on ready
@client.event
async def on_ready():
    print(f"\n{client.user.display_name} Ready", flush=True)

async def main():
    async with client:
        # load cogs
        for f in listdir("./cogs"):
            if f.endswith(".py"):
                await client.load_extension(f"cogs.{f[:-3]}")

        discord.utils.setup_logging(
            handler=LOG_HANDLER, level=logging_level, root=False)

        token = str(getenv("TOKEN"))
        await client.start(token)

if __name__ == "__main__":
    asyncio.run(main())
