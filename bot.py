#Code by Aki.no.Alice@Tyrant_Rex

import discord, os, asyncio

from discord.ext import commands
from os import getenv

prefix = getenv("PREFIX")
if not prefix:
    prefix = "-"

client = commands.Bot(command_prefix=prefix,activity=discord.Game(name="OniiChan's Heart"),intents=discord.Intents.all())

if not os.path.exists("./mp3"):
    os.mkdir("./mp3")

#on ready
@client.event
async def on_ready():
    print(f"\n{client.user.display_name}", flush=True)
    print("Ready", flush=True)

#on message
@client.event
async def on_message(message):
    if message.author != client.user:
        print(message.content, flush=True)
    await client.process_commands(message)

async def load():
    for f in os.listdir("./cogs"):
        if f.endswith(".py"):
            await client.load_extension(f"cogs.{f[:-3]}")

async def main():
    async with client:
        await load()
        await client.start("OTIyODYwNDc3MDU3NDc0NTcx.GdC3tk.8eNdptOrwsDTPbVbPgncMQGxdwe1GRLt6abhtc")

if __name__ == "__main__":
    asyncio.run(main())