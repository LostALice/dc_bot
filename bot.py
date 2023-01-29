#Code by Aki.no.Alice@Tyrant_Rex

import discord, os

from discord.ext import commands
from os import getenv

prefix = getenv("PREFIX")
if not prefix:
    prefix = "-"

client = commands.Bot(command_prefix=prefix,activity=discord.Game(name="OniiChan's Heart"))

if not os.path.exists("./mp3"):
    os.mkdir("./mp3")

#on ready
@client.event
async def on_ready():
    print(f"\n{client.user.display_name}",flush=True)
    print("Ready",flush=True)

if __name__ == "__main__":
    for f in os.listdir("./cogs"):
        if f.endswith(".py"):
            client.load_extension("cogs." + f[:-3])

    client.run("OTIyODYwNDc3MDU3NDc0NTcx.YcHmyw.169HGtV8pTeZTuAyvAo5-rvHmtw")

