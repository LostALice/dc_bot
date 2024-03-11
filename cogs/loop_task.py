# Code by AkinoAlice@Tyrant_Rex

from discord.ext import commands, tasks
from core.classes import Cog_extension
from datetime import datetime
from discord import Game


class LoopTask(Cog_extension):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.start_time: datetime = datetime.now()
        self.startup_timer.start()

    @tasks.loop(seconds = 1)
    async def startup_timer(self):
        execution_time = datetime.now() - self.start_time
        if self.client != None:
            await self.client.change_presence(
                activity=Game(
                    name=f"OniiChan's Heart for {execution_time.days} days"
                ))

async def setup(client: commands.Bot):
    await client.add_cog(LoopTask(client))