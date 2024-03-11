# Code by AkinoAlice@Tyrant_Rex

from core.classes import Cog_extension
from discord.ext import commands
from os import listdir


class Function(Cog_extension):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("Function.Function.py is ready")

    # aki daze!
    @commands.command(help="""Aki daze!""")
    async def aki(self, ctx) -> None:
        await ctx.message.delete()
        await ctx.channel.send(f"Ready DAZE My ping is {self.client.latency}!", delete_after=10)

class Debug(Cog_extension):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f"{__name__}.Debug is ready")
        for f in listdir("./cogs"):
            if f.endswith(".py"):
                await self.client.reload_extension(f"cogs.{f[:-3]}")
                print(f"cogs.{f[:-3]}")

    @commands.is_owner()
    @commands.command(aliases=["REL"], help="""For Bot Author Only""")
    async def rel(self, ctx) -> None:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        await ctx.message.delete()
        for f in listdir("./cogs"):
            if f.endswith(".py"):
                await self.client.reload_extension(f"cogs.{f[:-3]}")
                print(f"cogs.{f[:-3]}")
        await ctx.channel.send(f"Reloaded", delete_after=10)


async def setup(client):
    await client.add_cog(Function(client))
    await client.add_cog(Debug(client))
