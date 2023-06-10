#Code by AkinoAlice@Tyrant_Rex

import os

from discord.ext import commands
from core.classes import Cog_extension

class Function(Cog_extension):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("Function.Function.py is ready")

    #aki daze!
    @commands.command(help="""Aki daze!""")
    async def aki(self, ctx) -> None:
        await ctx.channel.purge(limit=1)
        await ctx.channel.send(f"Ready DAZE My ping is {self.client.latency}!", delete_after=10)

class Debug(Cog_extension):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("Function.Debug.py is ready")

    @commands.is_owner()
    @commands.command(help="""For Bot Author Only""")
    async def rel(self, ctx) -> None:
        await ctx.channel.purge(limit=1)
        for f in os.listdir("./cogs"):
            if f.endswith(".py"):
                await self.client.unload_extension(f"cogs.{f[:-3]}")
                await self.client.load_extension(f"cogs.{f[:-3]}")
        await ctx.channel.send(f"Reloaded", delete_after=10)
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

async def setup(client):
	await client.add_cog(Function(client))
	await client.add_cog(Debug(client))