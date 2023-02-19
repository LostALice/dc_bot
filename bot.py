#Code by Aki.no.Alice@Tyrant_Rex

import discord, os

from os import getenv
from discord.ext import commands

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

#on message
@client.event
async def on_message(message):
    if message.author != client.user:
        print(message.content,flush=True)
    await client.process_commands(message)

if __name__ == "__main__":
    for f in os.listdir("./cogs"):
        if f.endswith(".py"):
            client.load_extension("cogs." + f[:-3])

    client.run(getenv("TOKEN"))

