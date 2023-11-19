# Code by Aki.no.Alice@Tyrant_Rex

import asyncio
import discord
import logging
import os

from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

# logging
LOG_HANDLER = logging.FileHandler(
    filename="discord.log", encoding="utf-8", mode="w")

load_dotenv(".env.dev")
prefix = getenv("PREFIX")
if not prefix:
    prefix = "-"

client = commands.Bot(
    command_prefix=commands.when_mentioned_or(prefix),
    activity=discord.Game(
        name="OniiChan's Heart"
    ),
    intents=discord.Intents.all()
)

# done in docker image remove in next update
if not os.path.exists("./mp3"):
    os.mkdir("./mp3")


@client.event
# on ready
async def on_ready():
    print(f"\n{client.user.display_name}", flush=True)
    print("Ready", flush=True)


async def main():
    async with client:
        # load cogs
        for f in os.listdir("./cogs"):
            if f.endswith(".py"):
                await client.load_extension(f"cogs.{f[:-3]}")

        discord.utils.setup_logging(
            handler=LOG_HANDLER, level=logging.INFO, root=False)
        await client.start(getenv("TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
