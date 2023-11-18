# Code by AkinoAlice@Tyrant_Rex

import discord
import re

from pytube import YouTube  # type: ignore
from discord.ext import commands


class Cog_extension(commands.Cog):
    # Cog class
    def __init__(self, client):
        self.client = client


class Song_infos(object):
    # Song class
    """
        Useless class
    """

    def __init__(self, youtube_url: str, creator: discord.Message.author) -> None:
        yt = YouTube(youtube_url)

        self.url = yt.watch_url
        self.duration = yt.length
        self.author = creator.display_name  # type: ignore
        self.title = re.sub(r"[\/\\\:\*\?\"\<\>\|\#]", "", yt.title)


class Msg2sql(object):
    # Message class
    """
        To  be
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
