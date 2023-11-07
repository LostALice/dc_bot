# Code by AkinoAlice@Tyrant_Rex

import discord
import re

from pytube import YouTube
from discord.ext import commands

# Cog class


class Cog_extension(commands.Cog):
    def __init__(self, client):
        self.client = client

# Song class


class Song_infos:
    """
        Useless class
    """

    def __init__(self, url: str, author: str) -> None:
        yt = YouTube(url)

        self.url = yt.watch_url
        self.duration = yt.length
        self.author = author.display_name
        self.title = re.sub(r"[\/\\\:\*\?\"\<\>\|\#]", "", yt.title)


# Message class
class Msg2sql:
    """
        Useless class
    """

    def __init__(self, msg) -> None:
        self.content = msg.content
        self.message_id = msg.id
        self.message_attachments = [i.url for i in msg.attachments]
        self.send_time = str(msg.created_at)

        self.server_name = msg.guild.name
        self.server_id = msg.guild.id

        self.channel_name = msg.channel.name
        self.channel_id = msg.channel.id

        self.user_id = msg.author.id
        self.author = msg.author.name
