# Code by AkinoAlice@Tyrant_Rex

import discord
import re

from pytube import YouTube  # type: ignore
from discord.ext import commands


# Cog class
class Cog_extension(commands.Cog):
    def __init__(self, client):
        self.client = client


# Song class
class Song_infos(object):
    """
        Useless class
    """

    def __init__(self, youtube_url: str, creator: discord.Message.author) -> None:
        yt = YouTube(youtube_url)

        self.url = yt.watch_url
        self.duration = yt.length
        self.thumbnail = yt.thumbnail_url
        self.author = creator.display_name  # type: ignore
        self.icon = creator.display_avatar.url  # type: ignore
        self.title = re.sub(r"[\/\\\:\*\?\"\<\>\|\#]", "", yt.title)


# Message class
class MsgWrapper(object):
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
