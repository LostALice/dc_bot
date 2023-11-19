# Code by AkinoAlice@Tyrant_Rex

import asyncio
import discord
import sqlite3
import random
import re
import os

# from pprint import pprint # debug
from discord.ext import commands


class SQLiteDatabase(object):
    def __init__(self, database, password):
        ...


class Statistics(commands.Cog):
    def __init__(self, client):
        ...


async def setup(client):
    await client.add_cog(Statistics(client))
